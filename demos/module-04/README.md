# Module 4 demo: persistent memory with Mem0

Used in `lectures/dsca-module-04.html`: slide 5 (Mem0's extract-and-update
mechanism) in the Lecture section, and slides 14 (storing facts), 15
(retrieval merged into citation), 16 (the two-session checkpoint), 17
(compaction), and 20 (the "forget me" stretch) in the Hands-on lab. One
script, `memory_demo.py`, runs against the real `mem0ai` package, not a
reimplementation: Mem0 is a named course tool per the syllabus, so the
point is showing the real library's actual behavior.

There is also `memory_demo.ipynb`, a self-study companion, not a
replacement. It imports `memory_demo.py`'s own functions rather than
copying them, so the two can never quietly drift apart. Run the script
live in the room for the persistence proof, two real terminal
invocations is the most convincing version of that argument. Hand
students the notebook afterward: markdown narration between each part,
and (once you have run it once yourself with saved output, see its own
first cell) the actual output already there to read without needing a
key or a live connection. Its one design wrinkle is worth knowing about
before you open it: a notebook's single kernel cannot repeat the
persistence proof by calling a function twice, that would only show a
new object was built, not that a process died and a new one still
remembered anything, so its Part 2 cell launches a real subprocess
instead, see that cell for why.

## One-time setup

Do this once, not per module (it is the same setup `../README.md` describes
for every demo in this folder): activate the shared `demos/.venv`, install
`../requirements.txt` (now including `mem0ai`), and confirm `GOOGLE_API_KEY`
is set in `demos/.env`. No extra credential beyond that: the vector store is
Qdrant running in local, on-disk mode, no server, no separate account.

## Run it

From the `demos/` folder, with the shared environment active:

```
python module-04/memory_demo.py
```

Each run starts from a clean store (the script deletes its own
`module-04/mem0_store/` folder first), so output is the same every time:

**Part 1, extraction and deduplication.** States "I'm based in Beirut,"
then a few turns later, "I just moved from Beirut to Paris for work."
Watch the second `memory.add()` result: its `event` should be `UPDATE`, not
a second `ADD`. This is slide 5's four-operation mechanism (ADD, UPDATE,
DELETE, NOOP) against a real call instead of a diagram.

**Part 2, a second session.** A brand-new `Memory` instance, built from
scratch with no Python state shared with the first one, searches for
"Where does the user currently live?" and finds the Paris fact. A real
process restart is what the lab checkpoint actually requires; this script
cannot fork a second OS process, so a fresh object pointed at the same
on-disk path is the honest stand-in, see the script's own docstring for why
that is a faithful test of the same property (the data lives on disk, not
in a Python object).

**Part 3, compaction.** A fake 25-turn conversation gets folded down to a
20-turn budget: the oldest 5 turns become one summary message instead of
being silently dropped or left to overflow. The summarizer here is a stub,
not a real Gemini call, so this part's logic can be tested without spending
a request every run; a real deployment would call the same model the rest
of the pipeline uses.

**Part 4, forget me.** Calls `delete_all` for the demo user, then actually
checks that both `search` and `get_all` come back empty afterward, rather
than trusting an error-free return value. This is the concrete answer to
"what happens when a user asks the agent to forget something," the Module
4 wrap discussion prompt.

## What to point at, live

- **Part 1** is the argument for extract-and-update over a flat message
  log: the system does not just append a new fact, it recognizes the
  second statement supersedes the first.
- **Part 2** is the whole point of persistent memory versus session
  memory: closing the codebase, or even the whole terminal, does not lose
  the fact.
- **Part 3** is the same problem the lecture's summarization slide poses:
  a long enough conversation would eventually exceed the model's context
  window if every turn stayed live forever.
- **Part 4** is the direct answer to the syllabus's own memory-failure-mode
  discussion question ("what happens when a user asks the agent to forget
  something"), verified rather than assumed.

## The one API asymmetry worth calling out explicitly

Current `mem0ai` (2.0.20 as of this writing) is not consistent about where
`user_id` goes: `memory.add()` and `memory.delete_all()` both take it as a
plain keyword argument, but `memory.search()` and `memory.get_all()` both
require it inside a `filters={"user_id": ...}` dict instead, and raise a
`ValueError` if it is passed at the top level. `memory_demo.py` gets this
right throughout; if you extend it, check which family a new call belongs
to before assuming the same calling convention carries over.

## Embedding model

The demo reads `EMBEDDING_MODEL` from `demos/.env`. Use
`models/gemini-embedding-001`, which supports Gemini's `embedContent` API
and produces the 768-dimensional vectors configured for the local Qdrant
store. The script uses that value by default when the environment variable
is absent.

## Swap in your own facts

`session_one()` and `session_two_recall_and_cite()` near the top of
`memory_demo.py` are the whole scenario: replace the two conversational
turns with your own team's domain (an order-status agent remembering a
customer's shipping address, a tutoring agent remembering a student's
current course), and the ADD/UPDATE/search/citation flow underneath is
unchanged.

## Quick check with no live discussion needed

The same command as above (`python module-04/memory_demo.py`) is also the
quick check: if it runs end to end, part 1 reports an `UPDATE` event, part
2 recalls Paris, part 3 shows exactly 20 output messages, and part 4 prints
`True`, the setup is working.
