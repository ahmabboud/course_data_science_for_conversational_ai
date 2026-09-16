# NotebookLM summary: Chan, Chen, Cheng & Huang, "Don't Do RAG" (WWW '25)

Produced by NotebookLM from `chan-2025-dont-do-rag.pdf`, delivered 2026-09-15.
Kept verbatim as the instructor received it, for reference. Every number in
it was checked against the paper's own Table 2 and Table 3 on 2026-09-15 and
matches exactly; see `PROGRESS.md` for which of these numbers made it into
the actual lecture deck and which did not.

## 1. The idea in one paragraph

Cache-Augmented Generation (CAG) is a retrieval-free architecture for
knowledge-intensive LLM tasks. Instead of dynamically retrieving text chunks
per query, CAG preloads an entire document collection into the extended
context window of a long-context LLM and precomputes its Key-Value (KV)
inference cache offline (`C_KV = KV-Encode(D)`). At runtime, the model
evaluates user queries directly against this persistent KV cache
(`A = M(q | C_KV)`), completely bypassing external vector databases, search
algorithms, and context assembly. Multi-turn or multi-query sessions are
maintained simply by truncating appended query/response tokens to reset the
cache state instantly.

## 2. The problem it responds to

Traditional Retrieval-Augmented Generation (RAG) introduces three core
bottlenecks:

- **Retrieval latency.** Searching, scoring, and reranking passages across
  external vector stores adds non-trivial per-query overhead.
- **Retrieval and selection errors.** Mis-ranking or omitting relevant
  chunks directly degrades LLM generation quality.
- **System complexity.** Managing separate embeddings, vector databases,
  chunking strategies, and generation models increases architecture and
  maintenance overhead.

As modern LLMs support context lengths of 32K to 128K+ tokens, manageable
knowledge bases (enterprise FAQs, internal manuals, customer support logs)
can fit entirely within context, making real-time chunk retrieval redundant.

## 3. How they tested it

- **Model and hardware:** Llama 3.1 8B (128K context window), evaluated on
  8x Tesla V100 32GB GPUs.
- **Datasets and scale:** two benchmarks across three context sizes.
  - SQuAD 1.0 (single-passage QA): Small (3 docs / 21k tokens), Medium
    (4 docs / 32k tokens), Large (7 docs / 50k tokens).
  - HotPotQA (multi-hop QA): Small (16 docs / 21k tokens), Medium
    (32 docs / 43k tokens), Large (64 docs / 85k tokens).
- **Baselines:** Sparse RAG (BM25) and Dense RAG (OpenAI indexes), each
  evaluated at top-1, top-3, top-5, and top-10, plus dynamic in-context
  learning (ICL) without KV caching.
- **Metrics:** BERTScore for response similarity, and response time in
  seconds, split into retrieval versus generation latency.

## 4. The actual results

- **Answer quality (BERTScore):**
  - HotPotQA: CAG outperformed all RAG configurations on Small (0.7951 vs.
    Sparse top-5 0.7676 / Dense top-3 0.7582) and Medium (0.7821 vs. Sparse
    top-5 0.7633 / Dense top-3 0.7432). On Large, CAG scored 0.7407,
    outperforming Dense RAG top-10 (0.7374).
  - SQuAD: CAG led on Small (0.7695 vs. Sparse top-3 0.7616), Medium
    (0.7383 vs. Sparse top-3 0.7301), and Large (0.7734 vs. Sparse top-5
    0.7658).
- **Latency:**
  - Zero retrieval time for CAG (0.0000s), versus 0.3803-0.4849s for Dense
    RAG across conditions.
  - Versus uncached in-context learning: HotPotQA Small 9.32s to 0.85s,
    Medium 26.37s to 1.41s, Large 92.08s to 2.26s.

## 5. Limitations stated by the authors

- **Corpus size ceiling.** CAG requires the document collection to fit
  within the LLM's context window, impractical for datasets exceeding
  context limits.
- **Long-context degradation.** As context size expands (HotPotQA Large),
  accuracy gains narrow, consistent with known long-context degradation
  ("lost in the middle").
- **Context generation overhead.** Retrieval time is zero, but generation
  time over the preloaded context grows with corpus size (0.85s at 21k
  tokens to 2.26s at 85k tokens).

## Two accompanying infographics (received as PNGs, not embedded in the deck)

NotebookLM also produced two infographic images,
`notebooklm-rag-vs-cag-reference-1.png` and `-reference-2.png` in this
folder. Both were checked against Table 2 and Table 3 of the paper: the
numbers they carry (the Large-condition retrieval/generation time table in
particular) are accurate. They are **kept here as instructor reference
only**, not wired into `lectures/dsca-module-03.html` as slides or figures.
See `PROGRESS.md`, Module 3 graphics track, for why: both images use
gradient fills, decorative stock-icon art (a brain icon, a padlock cube,
emoji-adjacent glyphs) and hardcoded colours outside `assets/lu.css`'s
tokens, which `AGENTS.md` §2 rules out for anything that ships as a slide
("no emoji, no gradient backgrounds, no invented icons," "no new colours...
in inline styles"). Reference 1 also captions itself "Source: Advanced AI
Architectures 2024," which is not this paper and is not a real citation;
that line should not reach a student-facing slide under any circumstance.
The verified numbers from both images were used instead to add a real
CAG-inclusive results table to the deck's own on-brand results slide.
