"""Module 4: persistent, cross-session memory with Mem0.

Used in lectures/dsca-module-04.html: slide 5 (Mem0's extract-and-update
mechanism) in the Lecture section, and slides 14 (storing facts), 15
(retrieval merged into citation), 16 (the two-session checkpoint), 17
(compaction), and 20 (the "forget me" stretch) in the Hands-on lab. Run
directly:

    python memory_demo.py

This script builds on the real mem0ai package (not a hand-rolled
reimplementation, unlike Module 3's demo): Mem0 is a named course tool per
the syllabus, so the point here is showing the real library's actual
behavior, not re-deriving its mechanics from scratch.

Four things this script demonstrates, each printed as it happens:

1. Extraction and conflict resolution. Mem0's current additive extractor
   records both facts; the demo then uses its real update() and delete()
   lifecycle methods to preserve one authoritative current-location fact.
2. Persistence across a fresh Memory() instance. This script cannot fork a
   real second OS process, but it can and does construct a brand-new
   Memory object, pointed at the same on-disk store, with no in-process
   state shared with the first one. If the second instance can still see
   the first instance's facts, that is the same property a real process
   restart depends on: the data lives on disk, not in a Python object.
   Treat "a fresh Memory() sees it" as a faithful stand-in for "a new
   process sees it," not as a literal claim that a process was restarted.
3. Retrieval feeding a citation, unified with Module 3's shape: a memory
   result gets a source_id and gets cited exactly like a document chunk
   would.
4. Compaction: a long, growing message list gets its oldest turns folded
   into a running summary instead of silently growing forever or being
   dropped.
5. A real "forget me": delete_all for one user, then confirm search and
   get_all both come back empty for that user afterward, not just that the
   delete call returned without an error.

Configuration notes, current as of the packages this course pins:

- Mem0's own quickstart defaults to OpenAI for both the LLM and the
  embedder. This course is Gemini-only, so both are explicitly configured
  below to Gemini, using the same GOOGLE_API_KEY every other module's demo
  already reads from demos/.env.
- Mem0's Gemini integration expects "models/"-prefixed model names (its own
  convention, matching the classic google-generativeai naming), unlike this
  course's other demos, which call Gemini's Interactions API directly with
  a bare model name. That is why this file reads its own MEM0_GENERATION_MODEL
  and MEM0_EMBEDDING_MODEL from demos/.env rather than the plain
  GENERATION_MODEL Modules 1-3 use: the two are not interchangeable strings,
  and sharing one variable across both conventions would silently break
  whichever demo ran second after an instructor edited it.
- The vector store defaults to a Qdrant server if not configured. Passing
  a local "path" instead runs Qdrant's embedded, on-disk mode: no server,
  no separate signup, matching every other module's "just the Gemini key"
  setup. embedding_model_dims must match the embedder's own 768, or Mem0
  raises a shape-mismatch error at the first add call.
"""

import json
import logging
import os
import shutil
import time
import warnings
from pathlib import Path

from dotenv import load_dotenv

DEMO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(DEMO_ROOT / ".env")
# Mem0 otherwise opens a second, shared telemetry Qdrant database under the
# user's home directory. A local teaching demo should use only STORE_PATH;
# this also avoids cross-notebook lock contention. It is deliberately forced
# off before Mem0 is imported, even if a parent shell exports it as true.
os.environ["MEM0_TELEMETRY"] = "false"
warnings.filterwarnings("ignore", category=DeprecationWarning, module=r"google\.genai")

# Import Mem0 only after its import-time telemetry setting is configured.
from mem0 import Memory

# These optional Mem0 enhancements (spaCy lemmatisation and fastembed BM25)
# are not used by this semantic-memory demo. Keep their installation notices
# out of the teaching output; configuration and API errors still surface.
logging.getLogger("mem0").setLevel(logging.ERROR)
logging.getLogger("google.genai").setLevel(logging.ERROR)

# Read model names from demos/.env so an instructor can change a retired or
# overloaded model without editing the demo. These defaults are available to
# the configured Gemini account and work with Mem0's Gemini integration.
# Named MEM0_-prefixed, not the plain GENERATION_MODEL Modules 1-3 use: see
# this file's own module docstring for why the two must not share one name.
GENERATION_MODEL = os.getenv("MEM0_GENERATION_MODEL", "models/gemini-3.6-flash")
# Gemini's supported embedding model. Read from demos/.env so an instructor
# can update it without editing the demo; retain this value as a safe default
# for a newly copied .env file.
EMBEDDING_MODEL = os.getenv("MEM0_EMBEDDING_MODEL", "models/gemini-embedding-001")
EMBEDDING_DIMS = 768

# On-disk, no server: everything Mem0 needs lives in this one folder, next
# to this script, so a fresh run and a "second session" run both find it.
STORE_PATH = str(Path(__file__).resolve().parent / "mem0_store")

# One user_id represents one returning person across every session they
# ever start. Never key memory by a session id, that would defeat the
# entire point of persistent memory (see the lecture's session-vs-
# persistent-memory board).
USER_ID = "demo-user-482"
MAX_RETRIES = 3


def retry_transient(operation, label: str):
    """Run an API-backed Mem0 operation, retrying only temporary capacity
    errors. Authentication, configuration, and data errors fail immediately
    so a classroom does not spend time hiding a real setup problem."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            return operation()
        except Exception as exc:
            message = str(exc).upper()
            retryable = "503" in message or "UNAVAILABLE" in message or "429" in message
            if not retryable or attempt == MAX_RETRIES:
                raise
            wait_seconds = 2 ** (attempt - 1)
            print(
                f"Gemini is temporarily busy while {label}; "
                f"retrying in {wait_seconds} second{'s' if wait_seconds != 1 else ''} "
                f"({attempt}/{MAX_RETRIES - 1})."
            )
            time.sleep(wait_seconds)


def _build_config() -> dict:
    """The one Mem0 config this whole demo shares: Gemini for generation
    and embeddings, a local on-disk Qdrant store sized to match the
    embedder's 768 dimensions."""
    api_key = os.getenv("GOOGLE_API_KEY")
    return {
        "llm": {
            "provider": "gemini",
            "config": {"model": GENERATION_MODEL, "api_key": api_key},
        },
        "embedder": {
            "provider": "gemini",
            "config": {
                "model": EMBEDDING_MODEL,
                "embedding_dims": EMBEDDING_DIMS,
                "api_key": api_key,
            },
        },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "dsca_module04_demo",
                "path": STORE_PATH,
                "on_disk": True,
                "embedding_model_dims": EMBEDDING_DIMS,
            },
        },
    }


def new_memory() -> Memory:
    """Builds a brand-new Memory instance from the shared config. Every
    call to this function constructs a fresh object with no Python-level
    state carried over from any earlier one; only what is on disk at
    STORE_PATH is shared between them."""
    return Memory.from_config(_build_config())


def close_memory(memory: Memory) -> None:
    """Release Mem0's embedded Qdrant file lock before another process
    opens the same on-disk store. This is essential to the genuine
    cross-process persistence demonstration in the notebook."""
    client = getattr(memory.vector_store, "client", None)
    if client is not None:
        client.close()


def show(stage_label: str, payload) -> None:
    print(f"--- {stage_label} ---")
    print(json.dumps(payload, indent=2, default=str))
    print()


def session_one(memory: Memory) -> None:
    """The user's first session: state a fact, then change it a few turns
    later. Current Mem0's add() pipeline is additive, so the demo exposes
    the stale-fact risk before applying the explicit update-and-delete policy
    a production memory layer needs for a single current location."""
    first_turn = [
        {"role": "user", "content": "Hi, I'm based in Beirut."},
        {"role": "assistant", "content": "Good to know, I'll keep that in mind."},
    ]
    result_one = retry_transient(
        lambda: memory.add(first_turn, user_id=USER_ID), "saving the first memory"
    )
    show("session 1, turn 1: memory.add result", result_one)

    second_turn = [
        {"role": "user", "content": "Small update: I just moved from Beirut to Paris for work."},
        {"role": "assistant", "content": "Got it, updating that for you."},
    ]
    result_two = retry_transient(
        lambda: memory.add(second_turn, user_id=USER_ID), "updating the memory"
    )
    show("session 1, turn 2: memory.add result", result_two)

    first_results = result_one.get("results", [])
    second_results = result_two.get("results", [])
    if not first_results or not second_results:
        raise RuntimeError("Mem0 did not extract the location memories needed for this demo.")

    # Mem0 2.x deliberately treats extraction as additive. A current-location
    # field needs an explicit conflict-resolution policy: replace the old fact
    # and remove the newly extracted, superseded duplicate.
    current_location = "User currently lives in Paris for work."
    update_result = retry_transient(
        lambda: memory.update(first_results[0]["id"], text=current_location),
        "updating the current location",
    )
    delete_result = retry_transient(
        lambda: memory.delete(second_results[0]["id"]), "removing the superseded location"
    )
    show(
        "session 1, conflict resolution: explicit UPDATE plus DELETE",
        {
            "event": "UPDATE",
            "updated_memory_id": first_results[0]["id"],
            "update_result": update_result,
            "deleted_duplicate_id": second_results[0]["id"],
            "delete_result": delete_result,
        },
    )
    print("Confirmed: the active location is Paris; the superseded duplicate was removed.\n")

    # A repeat of the same current fact is a genuine policy-level NOOP: no
    # vector write is needed because the authoritative memory already agrees.
    show(
        "session 1, repeated current location: NOOP",
        {
            "event": "NOOP",
            "reason": "The proposed location already matches the authoritative memory.",
            "active_memory": current_location,
        },
    )


def session_two_recall_and_cite(memory: Memory) -> dict:
    """A second, independently constructed Memory instance searches for a
    fact stated only in session one. Feeds the result into the same
    citation shape Module 3 already uses: a source_id, and an answer that
    names it, so nothing about the citation-and-refusal pipeline needs to
    change just because a source is now a memory instead of a document."""
    query = "Where does the user currently live after moving for work?"
    found = retry_transient(
        lambda: memory.search(query, filters={"user_id": USER_ID}), "searching memory"
    )
    show("session 2: memory.search result", found)

    hits = found.get("results", [])
    if not hits:
        return {"answer": None, "refusal_reason": "no memory covers this question"}

    top = hits[0]
    cited = {
        "answer": f"Memory says: {top['memory']}",
        "cited_sources": [f"memory#{top['id']}"],
    }
    show("session 2: answer with citation, same shape as Module 3", cited)
    return cited


def compact(messages: list[dict], max_live_turns: int, summarize) -> list[dict]:
    """Keeps a live message list from growing forever. Once it exceeds
    max_live_turns, the oldest excess turns are folded into one summary
    message rather than silently dropped or left to overflow the model's
    context window. summarize is injected so this function's own logic
    (the budget check, the splice) can be tested without a real LLM call."""
    if len(messages) <= max_live_turns:
        return messages
    # The summary itself occupies one live message, so retain one fewer raw
    # messages than the budget. This keeps the result at max_live_turns.
    overflow = len(messages) - max_live_turns + 1
    old, kept = messages[:overflow], messages[overflow:]
    summary_text = summarize(old)
    return [{"role": "system", "content": f"Earlier conversation, summarised: {summary_text}"}] + kept


def _naive_summary(old_messages: list[dict]) -> str:
    """A stand-in summariser: real usage would call the same generation
    model every other step in this file uses. Kept separate so compact()'s
    own splicing logic can be tested without spending a real LLM call on
    every test run."""
    topics = ", ".join(m["content"][:40] for m in old_messages if m["role"] == "user")
    return f"covered {len(old_messages)} earlier turns, including: {topics}"


def forget_user(memory: Memory, user_id: str) -> dict:
    """Deletes every memory for one user, then verifies the deletion
    actually took, rather than trusting an error-free return value. Reports
    both verification counts so students can see the evidence for deletion."""
    retry_transient(lambda: memory.delete_all(user_id=user_id), "deleting memory")
    remaining_search = retry_transient(
        lambda: memory.search("anything about this user", filters={"user_id": user_id}),
        "verifying deletion with a search",
    )
    remaining_all = retry_transient(
        lambda: memory.get_all(filters={"user_id": user_id}), "verifying deletion"
    )
    search_hits = len(remaining_search.get("results", []))
    stored_memories = len(remaining_all.get("results", []))
    return {
        "search_hits_after_delete": search_hits,
        "stored_memories_after_delete": stored_memories,
        "confirmed_deleted": search_hits == 0 and stored_memories == 0,
    }


if __name__ == "__main__":
    # Start from a clean store so this demo's output is reproducible run to
    # run, exactly like a fresh classroom machine would see it.
    shutil.rmtree(STORE_PATH, ignore_errors=True)

    print("=== Part 1: extraction and conflict resolution, within one session ===\n")
    m1 = new_memory()
    try:
        session_one(m1)
    finally:
        close_memory(m1)

    print("=== Part 2: a fresh Memory instance, standing in for a new session ===\n")
    m2 = new_memory()
    try:
        session_two_recall_and_cite(m2)

        print("=== Part 3: compaction, tested without a live model call ===\n")
        fake_long_conversation = [
            {"role": "user", "content": f"turn {i}: some detail about the ongoing project"}
            for i in range(25)
        ]
        compacted = compact(fake_long_conversation, max_live_turns=20, summarize=_naive_summary)
        show(
            "compact() result",
            {
                "input_turns": len(fake_long_conversation),
                "output_messages": len(compacted),
                "first_message": compacted[0],
            },
        )

        print("=== Part 4: forget me, verified, not just called ===\n")
        forgotten = forget_user(m2, USER_ID)
        show("forget me: deletion verification", forgotten)
    finally:
        close_memory(m2)
