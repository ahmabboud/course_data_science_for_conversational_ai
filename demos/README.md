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

## Folder convention

Each module's demo lives in its own `module-NN/` subfolder, named for the
lecture it belongs to (`module-01/` for `dsca-module-01.html`, `module-02/`
for `dsca-module-02.html`, and so on). That subfolder holds the demo itself
and anything specific to it (a small data file, a `langgraph.json`, a second
script). When you add a new module's demo, create its `module-NN/` folder
and add a row to the table below.

Shared setup (the one Gemini key every module's demo calls) lives once, at
this level, in `requirements.txt` and `.env.example`: a module's subfolder
does not get its own copy of either just because it is a new module. The one
exception is a demo whose tool has a genuinely different dependency floor
from the shared environment, not just different packages. `module-02/` is
that exception: `langgraph-cli` requires Python 3.10 or newer, and the
shared environment set up for `module-01/`'s notebook may still be on an
older Python (3.9 has come up on this course before, see
`../requirements.txt`'s own `google-genai` history for a similar floor
lesson). Forcing that floor onto every module's environment would risk
breaking a working notebook setup over a CLI tool only one module needs. So
`module-02/` gets its own `requirements.txt`, in its own subfolder, with a
comment saying why. That is a deliberate, documented exception, not the
default: do not add a per-module `requirements.txt` just because a module
happens to want one extra package that runs fine on the shared floor.

## Which demo belongs to which lecture

| Demo | Used in | Slides | What it shows |
|---|---|---|---|
| `module-01/hook_demo.ipynb` | `lectures/dsca-module-01.html` | 2 ("Before we watch this"), 3 ("The five stages, already in front of you") | A naive keyword bot losing its own booking mid-conversation, then a reference agent holding state correctly across the same correction. |
| `module-02/` (`raw_loop.py`, `graph.py` via `langgraph dev`) | `lectures/dsca-module-02.html` | 3 ("The raw agent loop, with nothing hidden"), 5 ("LangGraph: nodes, edges, and state as one object") | The same order-status agent built twice: a plain Python loop printing the messages array after every step, then a LangGraph graph (agent / tool / escalate nodes) traced live in Studio. |

Add a row here whenever a later module gets its own instructor demo. The
lecture file's own speaker notes should say when to switch to the demo
(search the `.html` for the demo's path to confirm the link both ways), and
the demo's own top comment or first cell should name the lecture file and
slide numbers back, the same way `module-01/hook_demo.ipynb` and
`module-02/graph.py` do. Neither direction of that link is optional: a demo
with no cross-reference is indistinguishable from an orphaned file six
months from now.

## One-time setup, per instructor machine

This setup is shared across every module's demo except where a module's own
subfolder says otherwise (currently `module-02/`, see above).

1. `cd demos`
2. Create a Python environment and select it as the kernel for whichever
   module notebook you open (in VS Code: the kernel picker in the top right
   of the notebook; in Jupyter Lab: `New > Python 3`, or select an existing
   kernel). For a non-notebook demo, activate the same environment in your
   terminal instead.
3. Run `pip install -r requirements.txt` in that environment. If the
   module's own subfolder has its own `requirements.txt` (currently
   `module-02/`), read that subfolder's own setup note first, it likely
   wants a separate environment, not this shared one.
4. Get a Gemini key: go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   sign in with a Google account, click "Create API key." No card, no
   purchase, the free tier is enough for every module's demos.
5. `cp .env.example .env`, then paste the key in as `GOOGLE_API_KEY`. This
   is the instructor's own key, separate from any team's key in their own
   project repository, and every module's demo reads it from here (a
   subfolder with its own environment, like `module-02/`, still points back
   at this same `.env`, it does not need its own copy of the key).
6. Confirm each module's demo runs end to end once, then save its output
   (a notebook's cell output, a terminal transcript, whatever the demo
   produces) as the safety net if the room's connection has a bad moment
   during that module's live session.

This `.venv`, `.env`, and any `__pycache__` this creates are gitignored at
the repository root. Never commit a real API key.

## Troubleshooting

`AttributeError: 'Client' object has no attribute 'interactions'`: your
installed `google-genai` is older than 2.3.0, the version this course's code
needs for the Interactions API. Run `pip install --upgrade -r requirements.txt`
(from the `demos/` folder, or the module's own subfolder if it has its own
`requirements.txt`) in that environment, then restart before rerunning.
`requirements.txt` now pins `google-genai>=2.3.0` for exactly this reason,
so a fresh environment installing from it for the first time will not hit
this; it only bites an environment where an older `google-genai` was
installed before this pin was added.

`module-02/`'s `langgraph dev` refuses to start, or `pip install` for it
fails on a package resolution error: check your Python version first
(`python --version`), `langgraph-cli` needs 3.10 or newer. This is exactly
why `module-02/` has its own `requirements.txt` and, in practice, wants its
own virtual environment rather than the one set up for `module-01/`'s
notebook.
