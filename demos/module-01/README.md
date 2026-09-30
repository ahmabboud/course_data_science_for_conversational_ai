# Module 1 demo: `hook_demo.ipynb`

Used in `lectures/dsca-module-01.html`, slides "Before we watch this" and
"Live demo: two bots". A naive keyword bot loses
its own booking mid-conversation, then a reference agent holds state
correctly across the same correction.

## Run it

1. One-time setup only, do this once for every module's demo, not per
   module: see `../README.md`'s "One-time setup" section (the shared
   `demos/.venv`, `requirements.txt`, and Gemini key in `demos/.env`).
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


# Module 1 demo: `extraction_demo.ipynb`

Used in the "Instructor demo" part of the lecture, slides "Step 3: choose test
sentences", "Step 4: run it and read the result" and "Step 5: choose what
happens when it fails". An instructor-led demo: nobody types in class.

It runs the three helpdesk test sentences through one structured-output call
(same call shape as `hook_demo.ipynb`, with a helpdesk schema), prints the
three checks from the slide for each one (valid shape, right values, null when
unsure), then shows the three fallback strategies by changing one variable
(`FALLBACK = "ask"`, `"default"` or `"escalate"`).

Run it the same way as `hook_demo.ipynb` (see above), and run it once before
class with a real connection, saving the output, as a safety net.

**Test status (2026-09-30):** the notebook's own logic was run against a
stand-in for the model (a fake `google.genai` client, `PYTHONPATH` trick as in
Modules 4 and 5): the happy path, a reply that fails validation, and all three
fallbacks behave as described. It has **not** been run against the live Gemini
API, so the instructor still owns that check: confirm the model returns
sensible values for the three sentences and that the `description` in each
field actually changes what it does. The slides say "what we hope for", not a
measured result, for exactly this reason.
