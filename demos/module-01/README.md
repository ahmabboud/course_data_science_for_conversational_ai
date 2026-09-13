# Module 1 demo: `hook_demo.ipynb`

Used in `lectures/dsca-module-01.html`, slides 2 ("Before we watch this") and
3 ("The five stages, already in front of you"). A naive keyword bot loses
its own booking mid-conversation, then a reference agent holds state
correctly across the same correction.

## Run it

1. One-time setup only, do this once for every module's demo, not per
   module: see `../README.md`'s "One-time setup" section (Python
   environment, `pip install -r ../requirements.txt`, Gemini key in `../.env`).
2. Open `hook_demo.ipynb` in Jupyter Lab, VS Code, or any notebook UI, and
   pick the environment from step 1 as its kernel.
3. Run all cells top to bottom. The first cell installs anything missing;
   the last two show the naive bot losing state, then the reference agent
   holding it.
4. Before the session: run it once end to end and save it with its output
   intact, that saved output is the safety net if the room's connection has
   a bad moment during the live session.

No `langgraph dev`, no CLI, nothing else to start: a notebook is the whole
demo.
