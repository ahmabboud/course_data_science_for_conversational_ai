# Module 5 demo: an evaluation harness for a team's own agent

Used in `lectures/dsca-module-05.html`: the Hands-on lab section, slides 18
through 25, which build exactly this harness's four pieces live. One script,
`eval_harness.py`, evaluates a small toy agent built from scratch for this
demo (a retail order-status lookup, the same domain flavor as tau-bench's
own retail split), not a reimplementation of any team's real agent: the
four probes underneath are what a team wires up against their own.

There is also `eval_harness.ipynb`, a self-study companion, not a
replacement. It imports `eval_harness.py`'s own functions rather than
copying them, so the two can never quietly drift apart. Run the script
live in the room, its printed stages are the most direct version of the
argument. Hand students the notebook afterward: markdown narration
between each part, plus a cell that pulls out one failing attempt's actual
tool result and reply so a "silent fault" is something they read, not just
a summary boolean, and a cell that puts the bias probe's two replies side
by side. Once you have run it once yourself with saved output (see the
notebook's own first cell), a student can read the actual output without
needing a key or a live connection, same convention as
`module-04/memory_demo.ipynb`.

## One-time setup

Do this once, not per module (it is the same setup `../README.md` describes
for every demo in this folder): activate the shared `demos/.venv`, install
`../requirements.txt` (no new package for this module: it reuses
`google-genai` and `mem0ai`, already installed for Modules 1-3 and 4), and
confirm `GOOGLE_API_KEY` is set in `demos/.env`.

## Run it

From the `demos/` folder, with the shared environment active:

```
python module-05/eval_harness.py
```

Each run writes `module-05/eval_scorecard.json` (gitignored, a fresh copy
every run) and prints every stage as it happens:

**Part 1 and 2, scripted regression set plus pass^k.** Two scenarios, an
order that has shipped (`A100`) and one still processing (`A101`), each run
three times (`PASS_K = 3`). The one tool call, `get_order_status()`, is
seeded to return a stale, wrong cached result on some calls (`FLAKE_RATE =
0.4`), reproducibly: rerunning this script produces the same stale/correct
pattern every time. A structured Gemini call then judges each full
trajectory (tool call and result, not just the final reply) against the
scenario's own known-correct expected outcome. Expect `order-shipped` to
show `pass_1: true, pass_3: false`, its seeded attempts 1 and 2 hit the
stale path, and `order-processing` to show `pass_1: true, pass_3: true`,
a clean control with no stale hits at this seed. If a live run produces
different numbers, that is a real, correct pass^k result, not a bug: the
whole point of this part is that pass^1 and pass^k can disagree.

**Part 3, bias probe.** The `order-shipped` scenario run twice with the
identical seed (so the tool's own result is byte-identical both times):
once with no persona cue, once with `PERSONA_CUE` (a retired factory
worker on a fixed income) prepended to the customer's opening line.
`delta_detected` is true only if the judged outcome differs between the
two, isolating the persona cue as the only variable, same as the lecture's
own bias-probing mechanism.

**Part 4, PII-leakage probe.** Plants a fake callback number for one user,
confirms a differently-scoped search for another user_id does not see it,
then calls Module 4's own `forget_user()` (imported, not reimplemented)
and trusts its verified-deletion result. Uses this module's own on-disk
Mem0 store (`module-05/mem0_store/`, gitignored), never Module 4's: the two
demos share code, not files.

## What to point at, live

- **Parts 1 and 2** are the whole lecture in miniature: a single scripted
  run can look perfect (`pass_1: true`) while the same scenario, repeated,
  reveals a real reliability problem the class can see for themselves,
  against this demo's own agent, not just in someone else's benchmark
  numbers.
- **Part 2's judge** is the direct answer to the research dive's own
  finding: it is explicitly given a known-correct expected outcome and
  asked to check the tool call against it, not just whether the final
  reply reads fluently, which is exactly the design an outcome-only judge
  lacks.
- **Part 3** is the bias-probing mechanism made concrete: same seed, same
  tool result, only the persona line differs.
- **Part 4** is the ethics/privacy rubric row's direct evidence: documented
  and demonstrated, not claimed.

## Why the toy agent is deliberately flaky

`get_order_status()`'s stale-cache path is not a bug to fix, it is the
point: it gives `pass_1` and `pass_3` a real chance to disagree, and gives
the step-rubric judge something a silent, fluent-sounding reply could
still get wrong. Swap this toy agent's tool call and reply generation for
your own team's agent; `pass_k_for_scenario()`, `bias_probe()`, and
`pii_leakage_probe()` do not need to change to run against it.

## Reusing Module 4's memory functions, not reimplementing them

`eval_harness.py` imports `close_memory`, `forget_user`, `retry_transient`,
and Module 4's own verified `MEM0_GENERATION_MODEL`/`MEM0_EMBEDDING_MODEL`
pair directly from `module-04/memory_demo.py` (added to `sys.path` at the
top of the file), rather than re-deriving the retry policy or the
verified-deletion check a second time. Only `new_memory()` is redefined
here, pointed at this module's own `mem0_store/` and its own collection
name, so the two modules' demos never share on-disk state even though they
share code.

## Quick check with no live discussion needed

The same command as above (`python module-05/eval_harness.py`) is also the
quick check: if it runs end to end, the regression summary shows two
scenarios with `pass_1`/`pass_3` booleans, the bias probe reports a
`delta_detected` boolean, and the PII probe reports `pii_probe_pass: true`,
the setup is working. `eval_scorecard.json` in this folder afterward is
the same JSON, saved.
