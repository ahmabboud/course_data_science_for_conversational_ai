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

**Test status (2026-09-30):** both notebooks were run against the live Gemini API
with no model override, on the course default `gemini-3.1-flash-lite` (the
cheapest text model that works; see `../README.md`), and saved with their
output (the install cell's output was cleared because it prints local paths).
Real results for the three helpdesk sentences: VPN gave outage, high, VPN;
"I cannot log in." gave access, null, null; the payroll sentence gave outage,
low, "payroll system", which the schema accepts (valid shape, doubtful value),
so the notebook adds a small rule of its own that asks when an outage is
marked "low". The hook demo's reference agent kept 4 and 7pm and changed only
the day. The deck says "what we hope for", because models and limits change:
run the notebook once before each session and keep the output on screen as a
safety net. Each call took about 5 to 7 seconds; the very first call of a
session can take longer (a cold start took 37 seconds once).
