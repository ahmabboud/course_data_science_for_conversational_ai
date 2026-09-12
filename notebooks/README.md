# Notebooks

Instructor-only demo notebooks. None of these are linked from the student-facing
site (`index.html`); students never open this folder. Each one is run live, or
pre-run with output saved as a safety net, during a specific lecture, never as
homework or a deliverable on its own.

## Which notebook belongs to which lecture

| Notebook | Used in | Slides | What it shows |
|---|---|---|---|
| `hook_demo.ipynb` | `lectures/dsca-module-01.html` | 2 ("Before we watch this"), 3 ("The five stages, already in front of you") | A naive keyword bot losing its own booking mid-conversation, then a reference agent holding state correctly across the same correction. |

Add a row here whenever a later module gets its own instructor notebook. The
lecture file's own speaker notes should say when to switch to the notebook
(search the `.html` for the notebook's filename to confirm the link both
ways), and the notebook's own first cell should name the lecture file and
slide numbers back, the same way `hook_demo.ipynb` does. Neither direction of
that link is optional: a notebook with no cross-reference is indistinguishable
from an orphaned file six months from now.

## One-time setup, per instructor machine

1. `cd notebooks`
2. Create a Python environment and select it as this notebook's kernel (in
   VS Code: the kernel picker in the top right of the notebook; in Jupyter
   Lab: `New > Python 3`, or select an existing kernel).
3. Run `pip install -r requirements.txt` in that environment, or run the
   notebook's own first code cell, which does the same thing.
4. `cp .env.example .env`, then fill in `OPENAI_API_KEY` or
   `ANTHROPIC_API_KEY`, either is enough, `hook_demo.ipynb` picks whichever
   is set (OpenAI first if both are, matching the team template's own
   `verify_setup.py`). This is the instructor's own key, separate from any
   team's key in their own project repository. See the main course
   `README.md`'s setup note for where to get a free trial credit.
5. Confirm the notebook runs end to end once, then save it with its output
   intact. That saved output is the safety net if the room's connection has a
   bad moment during the live session.

This `.venv`, `.env`, and any `__pycache__` this creates are gitignored at the
repository root. Never commit a real API key.
