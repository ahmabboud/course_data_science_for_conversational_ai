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
(`module-01/README.md`, `module-02/README.md`): this page covers the
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

1. Work from the repository root. Check your Python version: `python3 --version`. This course's demos need
   **3.10 or newer** (`langgraph-cli`'s floor, for Module 2's demo).
   Create a Python environment on 3.10+ and select it as the kernel for
   whichever module notebook you open (in VS Code: the kernel picker in the
   top right of the notebook; in Jupyter Lab: `New > Python 3`, or select an
   existing kernel). For a non-notebook demo, activate the same environment
   in your terminal instead.
2. Run `pip install -r demos/requirements.txt` in that environment. This installs
   everything every module's demo needs, not just the one you are about to
   run.
3. Get a Gemini key: go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   sign in with a Google account, click "Create API key." No card, no
   purchase, the free tier is enough for every module's demos.
4. `cp demos/.env.example demos/.env`, then paste the key in as `GOOGLE_API_KEY`. This
   is the instructor's own key, separate from any team's key in their own
   project repository, and every module's demo reads it from `demos/.env`.
5. Confirm each module's demo runs end to end once, then save its output
   (a notebook's cell output, a terminal transcript, whatever the demo
   produces) as the safety net if the room's connection has a bad moment
   during that module's live session.

The root `.venv`, `demos/.env`, and any `__pycache__` this creates are gitignored at
the repository root. Never commit a real API key.

## Troubleshooting

`AttributeError: 'Client' object has no attribute 'interactions'`: your
installed `google-genai` is older than 2.3.0, the version this course's code
needs for the Interactions API. Run `pip install --upgrade -r demos/requirements.txt`
in that environment, then restart before rerunning. `requirements.txt` now
pins `google-genai>=2.3.0` for exactly this reason, so a fresh environment
installing from it for the first time will not hit this; it only bites an
environment where an older `google-genai` was installed before this pin was
added.

`langgraph dev` (Module 2) refuses to start, or `pip install -r demos/requirements.txt`
fails on a package resolution error: check `python3 --version` first,
`langgraph-cli` needs 3.10 or newer, and that floor applies to this whole
shared environment now, not just Module 2's demo. If your existing
environment predates 3.10, create a new one on a newer interpreter and
reinstall (see step 1 above) rather than trying to patch the old one.
