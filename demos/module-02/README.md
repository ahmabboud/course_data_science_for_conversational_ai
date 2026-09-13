# Module 2 demo: raw loop, then LangGraph

Used in `lectures/dsca-module-02.html`: slide 3 ("The raw agent loop, with
nothing hidden") and slide 14 ("Walkthrough: the raw loop, one call at a
time") use `raw_loop.py`; slide 5 ("LangGraph: nodes, edges, and state as one
object") and slide 15 ("Walkthrough: the same behavior, now on LangGraph")
use `graph.py` via `langgraph dev`. Both build the same order-status agent,
once with nothing hidden, once on LangGraph with explicit state.

## One-time setup

Do this once, not per module (it is the same setup `../README.md` describes
for every demo in this folder):

1. From the repository root, run `cd demos` and activate its shared `.venv`
   with `source .venv/bin/activate`. **Module 2 needs Python 3.10 or newer**
   (`langgraph-cli`'s floor).
2. `python -m pip install -r requirements.txt`.
3. Get a Gemini key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   (sign in, click "Create API key," no card needed), then
   `cp .env.example .env` and paste it in as `GOOGLE_API_KEY`.
   The scripts and LangGraph Studio both read this shared demos `.env`.
   To use Studio, also add a free `LANGSMITH_API_KEY` from
   [LangSmith settings](https://smith.langchain.com/settings). Leave
   `LANGSMITH_TRACING=false` for this local demo unless you want runs stored
   in LangSmith.
4. **Only needed for Studio, not for `raw_loop.py` or `graph.py`'s own
   quick check below:** get a free LangSmith API key. Studio is a hosted
   page (`smith.langchain.com`) that connects to your local server, so it
   needs its own credential to authenticate that connection, separate from
   the Gemini key. Go to [smith.langchain.com](https://smith.langchain.com),
   sign up (no card required, the Developer plan is $0/seat with 5,000
   traces a month included, far more than one lecture's live demo uses),
   then create a key at
   [smith.langchain.com/settings](https://smith.langchain.com/settings).
   Add it to the same `demos/.env` as `LANGSMITH_API_KEY=lsv2...`.
   `langgraph dev` reads it from there.

## Run `raw_loop.py` (slides 3 and 14)

From the `demos/` folder, with the environment above active:

```
python module-02/raw_loop.py
```

Prints the messages array after every step: the user's turn, the model's
first decision, the tool result, and the model's final reply. No server, no
browser, nothing else to start.

## Run `graph.py` in LangGraph Studio (slides 5 and 15)

From this folder (`demos/module-02/`), same environment:

```
cd module-02   # only if you ran the command above from demos/ instead
langgraph dev
```

This starts a local server (default `http://127.0.0.1:2024`) and opens
LangGraph Studio in your browser, connected to that local server. In
Studio:

1. Pick the `dialogue_agent` graph (named in `langgraph.json`).
2. Start a new thread and use the Chat tab to send an input message, for example
   `can you check if order A100 shipped yet?` (the two fake orders in
   `graph.py` are `A100` and `A200`; anything else returns "no order found").
3. Step through the run: you will see the `agent` node decide, the `tool`
   node run the lookup and loop back, and the `agent` node answer, the
   exact board slide 5 describes. Send something outside order status (a
   billing dispute, say) to see the `escalate` node instead.

Stop the server with `Ctrl+C` when done. If `langgraph dev` refuses to
start or `pip install` fails on a resolution error, check
`python3 --version` again first, see `../README.md`'s troubleshooting
section. If Studio itself says something like "missing LangSmith API key"
or refuses to connect, that is step 4 above, not a Gemini or Python
problem: confirm `LANGSMITH_API_KEY` is actually in `demos/.env`, not just
`GOOGLE_API_KEY`.

## Quick check with no browser and no Studio

```
python graph.py
```

(from `demos/module-02/`) runs one turn through the compiled graph directly
and prints the resulting messages, useful to confirm the setup works before
a live session without opening Studio at all.
