# Notebooks

Instructor-only demo notebooks. None of these are linked from the student-facing
site (`index.html`); students never open this folder. Each one is run live, or
pre-run with output saved as a safety net, during a specific lecture, never as
homework or a deliverable on its own.

## Folder convention

Each module's notebook (or notebooks) lives in its own `module-NN/` subfolder,
named for the lecture it belongs to (`module-01/` for `dsca-module-01.html`,
`module-02/` for `dsca-module-02.html`, and so on). That subfolder holds only
the notebook itself and anything specific to it (a small data file, say). It
does not hold its own `requirements.txt` or `.env.example`, since every module
this course ships calls the same one Gemini key: those two files, and this
README, live once at this level and cover every module's notebook. When you
add a new module's notebook, create its `module-NN/` folder, do not add a new
requirements file next to it, and add a row to the table below.

## Which notebook belongs to which lecture

| Notebook | Used in | Slides | What it shows |
|---|---|---|---|
| `module-01/hook_demo.ipynb` | `lectures/dsca-module-01.html` | 2 ("Before we watch this"), 3 ("The five stages, already in front of you") | A naive keyword bot losing its own booking mid-conversation, then a reference agent holding state correctly across the same correction. |

Add a row here whenever a later module gets its own instructor notebook. The
lecture file's own speaker notes should say when to switch to the notebook
(search the `.html` for the notebook's filename to confirm the link both
ways), and the notebook's own first cell should name the lecture file and
slide numbers back, the same way `module-01/hook_demo.ipynb` does. Neither
direction of that link is optional: a notebook with no cross-reference is
indistinguishable from an orphaned file six months from now.

## One-time setup, per instructor machine

This setup is shared across every module's notebook, done once, not repeated
per module.

1. `cd notebooks`
2. Create a Python environment and select it as the kernel for whichever
   module notebook you open (in VS Code: the kernel picker in the top right
   of the notebook; in Jupyter Lab: `New > Python 3`, or select an existing
   kernel).
3. Run `pip install -r requirements.txt` in that environment, or run the
   notebook's own first code cell, which does the same thing from inside its
   `module-NN/` subfolder.
4. Get a Gemini key: go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey),
   sign in with a Google account, click "Create API key." No card, no
   purchase, the free tier is enough for every module's notebooks.
5. `cp .env.example .env`, then paste the key in as `GOOGLE_API_KEY`. This
   is the instructor's own key, separate from any team's key in their own
   project repository, and every module notebook reads it from here.
6. Confirm each module's notebook runs end to end once, then save it with its
   output intact. That saved output is the safety net if the room's
   connection has a bad moment during that module's live session.

This `.venv`, `.env`, and any `__pycache__` this creates are gitignored at the
repository root. Never commit a real API key.
