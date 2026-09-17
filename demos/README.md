# Demos

Instructor-only demo material. None of it is linked from the student-facing
site (`index.html`); students never open this folder. Each demo is run live,
or pre-run with output saved as a safety net, during a specific lecture,
never as homework or a deliverable on its own.

A demo does not have to be a notebook. Module 1's is a notebook because a
side-by-side naive-bot-vs-reference-agent comparison is naturally a notebook.
Module 2's is a LangGraph graph run through the `langgraph dev` CLI and
Studio, because the thing worth showing there is the actual graph, traced,
not cells of output. Pick whatever tool actually shows the concept; do not
default to a notebook out of habit.

**For exact, copy-pasteable run steps, see each module's own README**
(`module-01/README.md`, `module-02/README.md`, `module-03/README.md`,
`module-04/README.md`, `module-05/README.md`): this page covers the
one-time setup shared by all of them, not how to run any one demo.

## Folder convention

Each module's demo lives in its own `module-NN/` subfolder, named for the
lecture it belongs to (`module-01/` for `dsca-module-01.html`, `module-02/`
for `dsca-module-02.html`, and so on). That subfolder holds the demo itself,
its own `README.md` with exact run steps, and anything specific to it (a
small data file, a `langgraph.json`, a second script). It does not hold its
own `requirements.txt` or `.env.example`: every module's demo installs from
the one shared `requirements.txt` at this level and reads the shared
`demos/.env`. When a later module's tool needs a package the others don't, add it
to this shared file with a comment saying which module needs it, rather
than forking a second requirements file, even if that package has a
noticeably different floor than the rest (see `requirements.txt`'s own
comment on `langgraph-cli`'s Python 3.10+ floor for the current example).
When you add a new module's demo, create its `module-NN/` folder, write its
`README.md`, and add a row to the table below.

## Which demo belongs to which lecture

| Demo | Used in | Slides | What it shows |
|---|---|---|---|
| `module-01/hook_demo.ipynb` | `lectures/dsca-module-01.html` | 2 ("Before we watch this"), 3 ("The five stages, already in front of you") | A naive keyword bot losing its own booking mid-conversation, then a reference agent holding state correctly across the same correction. |
| `module-02/` (`raw_loop.py`, `graph.py` via `langgraph dev`) | `lectures/dsca-module-02.html` | 3 ("The raw agent loop, with nothing hidden"), 5 ("LangGraph: nodes, edges, and state as one object") | The same order-status agent built twice: a plain Python loop printing the messages array after every step, then a LangGraph graph (agent / tool / escalate nodes) traced live in Studio. |
| `module-03/grounded_rag.py` | `lectures/dsca-module-03.html` | 3 (hybrid search), 4 (reciprocal rank fusion), 6 (reranking), 8 (citation and refusal), 18, 19, 21, 22 (the matching hands-on lab walkthroughs) | A small fake FAQ knowledge base run through the full pipeline: BM25 plus vector search merged by reciprocal rank fusion, a reranking pass, then either a cited answer or a refusal, depending on a coverage check. |
| `module-04/memory_demo.py`, `module-04/memory_demo.ipynb` | `lectures/dsca-module-04.html` | 5 (Mem0's extract-and-update mechanism) in the Lecture section, 14, 15, 16, 17, 20 (the matching hands-on lab walkthroughs) | The real `mem0ai` package, configured with Gemini for both generation and embeddings and a local on-disk Qdrant store: Mem0's additive extractor records a changed fact, then the demo applies its real `update()` and `delete()` methods to preserve one current value. A real process restart recalls that value, a long message list gets compacted, and `delete_all` is verified, not just called. The script is the live demo; the notebook is a self-study companion that imports the script's own functions and proves persistence with a genuine subprocess. |
| `module-05/eval_harness.py` | `lectures/dsca-module-05.html` | 18 through 25 (the Hands-on lab's four build walkthroughs) | A small, deliberately flaky toy order-status agent, evaluated four ways: a scripted regression set with full trajectory capture and a pass^k run (a single seeded run shows `pass_1: true, pass_3: false` for one scenario), a structured Gemini judge grading each trajectory against a known-correct expected outcome rather than the final reply alone, a bias probe (identical seed, only a persona cue differs), and a PII-leakage probe that imports and reuses `module-04/memory_demo.py`'s own `close_memory()`, `forget_user()`, and verified Gemini model-name pair rather than re-deriving them. |

Add a row here whenever a later module gets its own instructor demo. The
lecture file's own speaker notes should say when to switch to the demo
(search the `.html` for the demo's path to confirm the link both ways), and
the demo's own top comment or first cell should name the lecture file and
slide numbers back, the same way `module-01/hook_demo.ipynb` and
`module-02/graph.py` do. Neither direction of that link is optional: a demo
with no cross-reference is indistinguishable from an orphaned file six
months from now.

## One-time setup, per instructor machine

This setup is shared across every module's demo, done once, not repeated
per module. Each module's own `README.md` assumes this is already done and
only adds the steps specific to running that one demo.

1. From the repository root, run `cd demos`, then check `python3 --version`.
   This course's demos need **Python 3.10 or newer** (`langgraph-cli`'s
   floor, for Module 2's demo). Create and activate the one shared demo
   environment with `python3 -m venv .venv` and `source .venv/bin/activate`.
   Select `demos/.venv` as the kernel for a notebook, or activate it in the
   terminal for a script or LangGraph demo.
2. With that environment active, run `python -m pip install -r requirements.txt`.
   This installs everything every module's demo needs, not just the one you
   are about to run.
3. Get a Gemini key: go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   sign in with a Google account, click "Create API key." No card, no
   purchase, the free tier is enough for every module's demos.
4. `cp .env.example .env`, then paste the key in as `GOOGLE_API_KEY`. This
   is the instructor's own key, separate from any team's key in their own
   project repository, and every module's demo reads it from `demos/.env`.
   Leave `GENERATION_MODEL`, `MEM0_GENERATION_MODEL`, and
   `MEM0_EMBEDDING_MODEL` at their defaults unless a model gets retired:
   `GENERATION_MODEL` is Modules 1-3's own bare-name model string, and the
   `MEM0_`-prefixed pair is Module 4's, in Mem0's own "models/"-prefixed
   format, see `module-04/README.md` for why the two are not interchangeable.
5. Confirm each module's demo runs end to end once, then save its output
   (a notebook's cell output, a terminal transcript, whatever the demo
   produces) as the safety net if the room's connection has a bad moment
   during that module's live session.

`demos/.venv`, `demos/.env`, and any `__pycache__` this creates are
gitignored. Never commit a real API key.

## Troubleshooting

`AttributeError: 'Client' object has no attribute 'interactions'`: your
installed `google-genai` is older than 2.3.0, the version this course's code
needs for the Interactions API. From `demos/`, run
`python -m pip install --upgrade -r requirements.txt`
in that environment, then restart before rerunning. `requirements.txt` now
pins `google-genai>=2.3.0` for exactly this reason, so a fresh environment
installing from it for the first time will not hit this; it only bites an
environment where an older `google-genai` was installed before this pin was
added.

`langgraph dev` (Module 2) refuses to start, or
`python -m pip install -r requirements.txt`
fails on a package resolution error: check `python3 --version` first,
`langgraph-cli` needs 3.10 or newer, and that floor applies to this whole
shared environment now, not just Module 2's demo. If your existing
environment predates 3.10, create a new one on a newer interpreter and
reinstall (see step 1 above) rather than trying to patch the old one.
