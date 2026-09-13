# Module 2 demo: raw loop, then LangGraph

Used in `lectures/dsca-module-02.html`: slide 3 ("The raw agent loop, with
nothing hidden") and slide 12 use `raw_loop.py`; slide 5 ("LangGraph: nodes,
edges, and state as one object") and slide 13 use `graph.py` via
`langgraph dev`. Both build the same order-status agent, once with nothing
hidden, once on LangGraph with explicit state.

## One-time setup

Do this once, not per module (it is the same setup `../README.md` describes
for every demo in this folder):

1. Work from the repository root and activate its `.venv`. **Module 2 needs
   Python 3.10 or newer** (`langgraph-cli`'s floor).
2. `pip install -r demos/requirements.txt`.
3. Get a Gemini key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
   (sign in, click "Create API key," no card needed), then
   `cp demos/.env.example demos/.env` and paste it in as `GOOGLE_API_KEY`.
   The scripts and LangGraph Studio both read this shared demos `.env`.

## Run `raw_loop.py` (slides 3 and 12)

From the `demos/` folder, with the environment above active:

```
python module-02/raw_loop.py
```

Prints the messages array after every step: the user's turn, the model's
first decision, the tool result, and the model's final reply. No server, no
browser, nothing else to start.

## Run `graph.py` in LangGraph Studio (slides 5 and 13)

From this folder (`demos/module-02/`), same environment:

```
cd module-02   # only if you ran the command above from demos/ instead
langgraph dev
```

This starts a local server (default `http://127.0.0.1:2024`) and opens
LangGraph Studio in your browser, connected to that local server. In
Studio:

1. Pick the `dialogue_agent` graph (named in `langgraph.json`).
2. Start a new run with an input message, for example
   `can you check if order A100 shipped yet?` (the two fake orders in
   `graph.py` are `A100` and `A200`; anything else returns "no order found").
3. Step through the run: you will see the `agent` node decide, the `tool`
   node run the lookup and loop back, and the `agent` node answer, the
   exact board slide 5 describes. Send something outside order status (a
   billing dispute, say) to see the `escalate` node instead.

Stop the server with `Ctrl+C` when done. If `langgraph dev` refuses to
start or `pip install` fails on a resolution error, check
`python3 --version` again first, see `../README.md`'s troubleshooting
section.

## Quick check with no browser and no Studio

```
python graph.py
```

(from `demos/module-02/`) runs one turn through the compiled graph directly
and prints the resulting messages, useful to confirm the setup works before
a live session without opening Studio at all.
