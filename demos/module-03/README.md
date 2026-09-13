# Module 3 demo: hybrid search, reranking, citation, and refusal

Used in `lectures/dsca-module-03.html`: slide 3 (hybrid search), slide 4
(reciprocal rank fusion), slide 6 (reranking), and slide 8 (citation and
the refusal path) in the Lecture section, and slides 18, 19, 21, and 22
(the matching build walkthroughs) in the Hands-on lab. One script,
`grounded_rag.py`, builds a small fake FAQ knowledge base and runs the
whole pipeline the lecture describes against it.

## One-time setup

Do this once, not per module (it is the same setup `../README.md` describes
for every demo in this folder): activate the shared `demos/.venv`, install
`../requirements.txt`, and confirm `GOOGLE_API_KEY` is set in `demos/.env`.
No extra credential beyond that: unlike Module 2's `langgraph dev`, this
demo is a plain script with nothing else to authenticate.

## Run it

From the `demos/` folder, with the shared environment active:

```
python module-03/grounded_rag.py
```

This runs three questions through the full pipeline, printing the state
after every stage (BM25 hits, vector hits, the fused ranking, the reranked
top 3, the coverage check, then the final answer or refusal):

1. **"What is the warranty period for electronics?"** An exact-term
   question. Watch BM25 alone already surface the right document
   (`faq.md#warranty`); this is the case keyword search is naturally good
   at.
2. **"I bought a blender during a clearance sale and it turned out to be
   broken, can I send it back for a refund?"** A paraphrase of the returns
   policy that shares almost no exact words with it ("clearance" for
   "sale," "broken" for nothing in the source at all, "send it back" for
   "returned"). Compare this run's BM25 hits against its vector hits: this
   is the case vector search is supposed to catch and keyword search
   often ranks lower.
3. **"Do you price-match a lower price found at a competitor's store?"**
   Not covered anywhere in the six-entry FAQ. The coverage check should
   report `"covered": false`, and the final result should be a refusal
   with a specific reason, not a guess.

## What to point at, live

- **Step 1 vs step 2** on the first two questions is the hybrid-search
  argument made concrete: run either retrieval mode alone in a Python
  shell (`from grounded_rag import bm25_search, vector_search`) and show a
  case where it misses, before showing the fused result catching it.
- **Step 4** is the reranking pass. This demo reranks with one more Gemini
  call instead of a dedicated cross-encoder model, see the top of
  `grounded_rag.py` for why: it keeps the whole file on the same
  `google-genai` client every other demo in this course already needs,
  rather than adding a model-serving dependency for one pass. Say this
  plainly if asked why there is no `sentence-transformers` import.
- **Step 5 and step 6** on the third question are the refusal path. If a
  team asks "what if the coverage check is wrong," that is a real,
  legitimate question: this is exactly the kind of call worth testing
  against your own team's actual source material and actual hard
  questions, not just trusting it blind.

## Swap in your own source material

`FAQ` near the top of `grounded_rag.py` is the entire knowledge base: a
plain Python list of `{"source_id": ..., "text": ...}` entries. Replace it
with your team's own material and everything else, indexing, fusion,
reranking, citation, refusal, works unchanged. Keep `source_id` meaningful
(which document, which section) since that is exactly what ends up in a
citation.

## Quick check with no live discussion needed

The same command as above (`python module-03/grounded_rag.py`) is also the
quick check: if it runs end to end and question 3 comes back as a refusal
while questions 1 and 2 come back with a citation, the setup is working.
