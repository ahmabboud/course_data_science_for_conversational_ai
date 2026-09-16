# Progress tracker, Data Science for Conversational AI

Read this file first, before touching a module. It is the single place that
says what is done, what is in flight, and what a new session should pick up
next. Update it in the same turn as any work it describes, do not let it
drift behind the actual state of the repository.

This tracker exists because of four standing quality bars the instructor
set for every module, on top of the mechanical authoring contract in
`AGENTS.md`:

0. **Lecture notes come first.** Before any slide gets written, the module's
   full teaching content exists as its own markdown document,
   `research/module-NN/lecture-notes.md`. This one document does three jobs:
   it is the source the slide deck's prose gets pulled from, it is the
   source handed to NotebookLM to produce the concept-infographic slides
   (§2 below), and it is posted for students as extended reading in its own
   right. Skipping straight to slide-by-slide drafting (what happened for
   Module 3, before this rule existed) means the concept infographic has no
   real source to build from and the deck's prose has no single place it
   was drafted against.
1. **Research dive**: the module's research section must build around a
   real, open-access, important paper, explained so anyone can follow it in
   about five slides. Not a summary of a summary, a real close read. The
   paper doubles as the source for a NotebookLM research-infographic prompt.
2. **Graphics**: the concept-explanation graphics must be high quality, not
   the bare CSS primitives look. NotebookLM needs a source document to
   generate an infographic from, it does not invent one from a bare
   instruction; that source is the module's own `lecture-notes.md` (item 0),
   not the slide deck and not a one-line prompt. The resulting infographic
   ships as its own full-page slide (see Module 3's two examples), not
   traced or forced into a `.lu-board` redraw. CSS primitives and inline SVG
   (`AGENTS.md` §7) are still the right tool for a diagram genuinely simple
   enough to hand-draw on brand; the infographic route is for the ones that
   are not.
3. **Code**: every demo script must be tested before it is called ready, and
   commented well enough that an instructor who did not write it can run and
   explain it live. The instructor runs the tests and owns readiness
   sign-off; this repository's job is to keep each demo's `README.md`
   accurate and to record the test/readiness status here.

## The module build order (standing process, Module 4 onward)

1. Pull the module's row from the syllabus (`AGENTS.md` §0, `PROMPT.md`):
   objective, segments and minutes, deliverable, reading.
2. Write `research/module-NN/lecture-notes.md`: the full content in prose,
   organised by the syllabus's own segments, at the depth bar `AGENTS.md`
   §12 sets for a slide, formula, cost, alternative, and metric included,
   not just named. This is not slide-shorthand, it reads as a real, if
   compact, lecture text a student could learn from without the deck.
3. Find and download one open-access, important paper for the research
   dive; save it to `research/module-NN/<first-author>-<year>-<slug>.pdf`.
4. Produce two NotebookLM prompts and hand both to the instructor:
   - one sourced from the paper (PDF upload), for a research-infographic
     and markdown summary, same shape as Module 3's paper-track prompt;
   - one sourced from `lecture-notes.md` (paste or upload the markdown), for
     a concept infographic covering that module's hardest-to-draw ideas.
   Log both deliveries in this file's per-module section, same convention
   as Module 3, so a later session does not resend a duplicate.
5. Only after 1 to 4 exist, build the slide deck (`AGENTS.md` §1's steps),
   pulling slide prose from `lecture-notes.md` rather than drafting it fresh
   against the syllabus row directly. Add each infographic as its own
   full-page slide once it comes back (pattern in `PROMPT.md`'s image-slide
   recipe), not embedded mid-diagram.
6. Build the labs and demos, keep `demos/module-NN/README.md` current, hand
   the instructor the code-testing prompt (Code track below).

## Division of labor

- **Lecture-notes track**: an agent drafts `research/module-NN/lecture-notes.md`
  from the syllabus row, at the `AGENTS.md` §12 depth bar. This is the one
  track that is pure agent-authored content, not a delivered prompt; the
  instructor reviews and edits it like any other drafted document.
- **Paper track**: an agent searches for an important, open-access paper per
  module, downloads the PDF into `research/module-NN/`, and hands the
  instructor a NotebookLM prompt (source: the PDF) to turn it into a
  markdown summary and a research infographic.
- **Graphics track**: an agent hands the instructor a NotebookLM prompt keyed
  to `lecture-notes.md` as the source, for the concept infographic, for the
  instructor to run themselves. An agent does not invent a graphics prompt
  with no source document behind it.
- **Code track**: an agent keeps each demo's `README.md` current as the code
  changes, and hands the instructor a prompt for their own coding agent to
  add tests and comments to a demo script. The instructor runs the tests and
  updates the status below; an agent should not mark a module's code
  "tested" or "ready" on its own say-so.

## Status by module

| # | Title | Lecture notes | Paper | Graphics | Code |
|---|---|---|---|---|---|
| 1 | Foundations and Modern Understanding | Not started | Not started | Not started | Not started |
| 2 | Agentic Dialogue Management | Not started | Not started | Not started | Not started |
| 3 | Grounded Generation | Not written (predates this rule, slides came first) | Done, see below | In progress | In progress |
| 4 | Memory | Done, see below | Done, see below | In progress | Not started |
| 5 | Evaluation and Responsible Deployment | Not started | Not started | Not started | Not started |

Module 6 has no lecture deck (live defense session), so it carries no row
here; see `README.md`.

## Module 3, Grounded Generation, detail

### Paper track — done

- **Paper:** Chan, Chen, Cheng, and Huang, "Don't Do RAG: When Cache-Augmented
  Generation is All You Need for Knowledge Tasks," accepted at the Web
  Conference 2025 (WWW '25) as a short paper. Open access on arXiv
  (`2412.15605`).
- **Why this paper:** it is the paper the deck's research dive
  (`lectures/dsca-module-03.html`, "Part 2 · One paper says you might not
  need any of this," 6 slides including the divider) is already built
  around: the idea, the challenge, the experiment, the results, and the
  limits, each on its own slide, all read from the paper's own text and
  results table rather than a paraphrase. This already lands inside the
  "around five slides, anyone can follow it" bar.
- **Downloaded to:** `research/module-03/chan-2025-dont-do-rag.pdf`.
- **NotebookLM prompt:** sent to the instructor in chat on 2026-09-15. Run
  the same day. Output: a markdown summary (saved to
  `research/module-03/chan-2025-notebooklm-summary.md`) and two infographic
  PNGs (`research/module-03/notebooklm-rag-vs-cag-reference-1.png` and
  `-reference-2.png`). Every number in the summary and both images was
  checked against the paper's own Table 2 (BERTScore) and Table 3 (response
  time) on 2026-09-15 and is accurate. Outcome: the numbers were used to add
  a real, previously-missing CAG-inclusive results table to
  `lectures/dsca-module-03.html`'s results slide (see Graphics track below
  for why the images themselves were not embedded). Closed.

### Graphics track — in progress

- Current state: the research-dive and lecture slides use the CSS
  primitives (`.lu-board`, `.lu-node`, `.lu-svg`) per `AGENTS.md` §7, no
  `.lu-figure__ph` placeholders. Functional, but several concept slides
  (hybrid search's two-lane retrieval, reciprocal rank fusion's merge,
  CAG's preload-vs-retrieve contrast) would teach faster with a richer
  infographic than the current board/node treatment.
- **NotebookLM prompt:** sent to the instructor in chat on 2026-09-15, for
  the hybrid-search-plus-RRF concept and the CAG-vs-RAG contrast. Run the
  same day, two PNGs came back (see paper track above for file names).
- **Decision: not embedded in the deck, kept as instructor reference only.**
  Both images use gradient fills, decorative stock icons (a brain, a padlock
  cube, emoji-adjacent glyphs) and hardcoded colours outside `assets/lu.css`,
  which `AGENTS.md` §2 rules out for anything that ships as a slide ("no
  emoji, no gradient backgrounds, no invented icons," "no new colours... in
  inline styles"). They also cannot adapt to the paper/night grounds or
  print handout the way a CSS primitive or inline SVG does. Reference 1
  additionally captions itself "Source: Advanced AI Architectures 2024,"
  which is not a real citation for this paper and must never reach a
  student-facing slide. The underlying numbers were verified accurate and
  used instead in the results slide (paper track, above).
- **First attempt (redrawn on-brand `.lu-board`) tried and reverted,
  2026-09-15.** Rebuilt "The idea" slide's diagram as a three-row on-brand
  board (RAG / CAG-offline / CAG-online). Passed the automated audit clean,
  but the instructor's own read was "very bad," reverted in the same
  session back to the original two-row board. Lesson for next time: passing
  `scripts/audit-deck.js` is necessary, not sufficient, get a look from the
  instructor before treating a redraw as done, especially for a diagram this
  information-dense.
- **Shipped instead: the NotebookLM infographic as its own full-page slide,
  2026-09-15.** New slide "Infographic: RAG vs CAG at a glance" right after
  "The idea," in `lectures/dsca-module-03.html`. Uses
  `notebooklm-rag-vs-cag-reference-2.png` (the one with no fabricated
  citation), copied and downsized to `assets/img/m03-rag-vs-cag-infographic.png`
  (1400x1400, this is the real, on-repo asset path per `AGENTS.md` §0's
  `assets/img/` convention, not a placeholder). Framed as a supplementary
  visual aid, not a slide making its own claims: the caption says plainly
  it is not a figure from the paper, points to the paper itself, and links
  to the full-resolution image (`target="_blank"`) so it can be opened
  full-page and zoomed during class. Deliberately does NOT use
  `.lu-figure__frame` (that class is built for `object-fit:cover` photo
  captures and silently cropped this square infographic against a wide
  slide; fought it for a while, gave up and used a plain sized `<img>`
  instead, `max-height` plus `width/height:auto`, centered). Verified with
  `scripts/audit-deck.js`: no overflow (first pass at `max-height:520px`
  overflowed the footer by 70px, fixed at `420px` plus a shorter caption).
  Slide budget rebalanced back to 180 minutes by trimming the flexible
  "Now, build" lab slide from 27 to 25 minutes.
- **Hybrid search + RRF + reranking infographic shipped, 2026-09-15.** Same
  treatment, one new slide, "Infographic: the full retrieval pipeline, at a
  glance," placed right after the reranking slide (all three concepts it
  covers have been taught by then) and before the chunking slide. Image:
  `notebooklm-hybrid-search-rrf-reranking-reference.png` in `research/`,
  downsized to `assets/img/m03-hybrid-search-rrf-reranking-infographic.png`.
  This image has no baked-in citation, but it does carry an illustrative
  precision/latency/cost comparison table with numbers not measured from
  anything in this course; the caption and speaker notes say plainly they
  are illustrative, not a result to quote, so a team does not later cite a
  NotebookLM-invented 0.47 precision figure as if it were this course's own
  measurement. Verified with `scripts/audit-deck.js`: first pass at
  `max-height:460px` overflowed by 10px, fixed at `430px`. Slide budget
  rebalanced back to 180 minutes by trimming "Now, build" from 25 to 23
  minutes (now trimmed twice, from an original 27, for two infographic
  slides; if a third one is added later this slide cannot absorb much more
  without cutting into the lab itself).

### Known pre-existing issues, found while auditing 2026-09-15

Not introduced by this session's edits (re-confirmed after both
infographic-slide insertions shifted numbering twice; slide numbers below
are current as of this session's final state, 31 slides total). Not yet
fixed:

- **Slide overflow** on slide 3 (hybrid search), 6 (reranking), 9 (citation
  and refusal), 12 (the idea, CAG board, 351px), 15 (the experiment), 17
  (the limits), and 26 (likely bugs). Content is clipped with no scrollbar
  in at least one state (baseline or revealed). (Slide 5, the hybrid
  search/RRF check question, has flickered in and out of this list between
  audit runs on otherwise-unchanged content, worth a second look rather
  than trusting either result alone.)
- **Stray SVG edge endpoints** on slide 3 (41px off), slide 6 (138px off),
  and slide 12 (four endpoints, 81 to 157px off): an edge in the board's
  diagram does not actually reach a node.

A future pass on this module should fix these before calling the deck done,
per `AGENTS.md` §1 step 7. Slide 12 specifically is the original,
unmodified "the idea" board (the redraw attempt above was reverted); its
overflow and stray edges are old debt, not something introduced by
reverting to it.

### Code track — in progress

- **Demo:** `demos/module-03/grounded_rag.py`, backing slides 3, 4, 6, 8,
  18, 19, 21, 22. `README.md` in the same folder is current as of
  2026-09-15 (matches the script's actual stages and example questions).
- **Tests:** none exist yet. No `test_*.py`, no `pytest` config scoped to
  this script. The three example questions in `README.md` are a manual
  smoke check ("if question 3 comes back a refusal and 1/2 come back cited,
  it works"), not an automated test.
- **Prompt for the instructor's coding agent:** sent in chat on
  2026-09-15, to add automated tests (BM25-favoring, vector-favoring, and
  refusal cases; RRF math; coverage-check edge cases) and to comment the
  trickier stages, without changing the demo's teaching shape.
- **Readiness:** not ready. The instructor owns running the coding agent's
  output and the tests; update this line to "ready, tests passing as of
  <date>" once that happens, or note what failed.

## Module 4, Memory, detail

Planned 2026-09-15, following the module build order above (this is the
first module built under that process; nothing in this section has been
turned into slides yet).

### Syllabus row (Session 4, from the syllabus docx)

- **Objective.** Let the agent remember, across turns and across separate
  sessions, without quietly becoming a privacy liability.
- **Segments.** Lecture 50 min (session vs persistent memory, the
  extract-and-update pattern and the temporal-knowledge-graph pattern with
  Mem0 and Zep as working examples, summarization and compaction, privacy
  cost previewing Module 5); Hands-on lab 100 min (add persistent memory,
  recognize a returning user across two separate sessions, add
  summarization so long conversations do not overflow); Discussion and wrap
  30 min (memory failure modes: stale facts, wrong recall, forget requests;
  Issue 4 checkpoint). Total 180, matching Module 3's internal
  lecture/research-dive split pattern: propose ~30 min core concepts + ~20
  min research dive inside the 50-minute Lecture line.
- **Deliverable (Issue 4).** The team's agent demonstrably remembers a
  specific user across two separate sessions, with a working compaction
  strategy for long conversations.
- **Reading.** "On Memory Construction and Retrieval for Personalized
  Conversational Agents" (this module's research-dive paper). Mem0 and Zep
  documentation.
- **Rubric row (Memory, 15 pts).** The agent correctly recalls a specific
  user across two separate sessions, and long conversations are compacted
  rather than silently truncated or overflowed.

### Lecture-notes track — done

- **Written to:** `research/module-04/lecture-notes.md`. Covers session vs
  persistent memory, the extract-and-update pattern (Mem0), the
  temporal-knowledge-graph pattern (Zep/Graphiti), summarization and
  compaction, privacy cost, the full SeCom research-dive close read, the
  hands-on lab's planned build order, and the discussion-and-wrap failure
  modes, at the `AGENTS.md` §12 depth bar (formalism for each pattern, real
  cost numbers, named alternatives, a critical read of two papers, not just
  the one required reading).
- **Not yet done:** instructor review and edit. Per this file's own
  division of labor, an agent drafts this document but the instructor
  reviews it like any other drafted document before it becomes the source
  for slides or a NotebookLM prompt. Do not treat it as final until that
  happens.

### Paper track — done

- **Paper:** Pan, Wu, Jiang, Luo, Cheng, Li, Yang, Lin, Zhao, Qiu & Gao,
  "On Memory Construction and Retrieval for Personalized Conversational
  Agents," published as a conference paper at ICLR 2025. Open access on
  arXiv (`2502.05589`). This is the exact paper named in the syllabus's own
  Module 4 reading line, same selection logic as Module 3 (Chan et al. was
  also the syllabus's own named reading).
  Downloaded to `research/module-04/pan-2025-secom-memory.pdf`.
- **Two supporting papers also downloaded**, for the lecture's two named
  working examples, not as the research-dive paper: Chhikara et al. (2025),
  "Mem0: Building Production-Ready AI Agents with Scalable Long-Term
  Memory," arXiv:2504.19413 (`research/module-04/chhikara-2025-mem0.pdf`),
  and Rasmussen et al. (2025), "Zep: A Temporal Knowledge Graph Architecture
  for Agent Memory," arXiv:2501.13956
  (`research/module-04/rasmussen-2025-zep-graphiti.pdf`). Both verified by
  extracting their own PDF text on 2026-09-15, same standard as the
  research-dive paper; their numbers are in `lecture-notes.md` above.
- **NotebookLM prompt:** not yet sent. Send once the instructor has
  reviewed `lecture-notes.md` (paper track's prompt is independent of that
  review, but sending it before the notes are confirmed risks basing the
  concept-infographic prompt, tracked separately below, on content that is
  about to change).

### Graphics track — in progress, verification done, not yet shipped

- The instructor ran NotebookLM against `lecture-notes.md` before a formal
  prompt was sent (the "send a prompt" step in the build order was
  overtaken by the instructor just doing it); five images came back
  2026-09-15, saved to `research/module-04/notebooklm-reference/`:
  `mem0-infographic.png`, `zep-infographic.png`, `secom-infographic.png`,
  `session-vs-persistent-infographic.png`, and
  `combined-scorecard-infographic.png` (one table comparing all three
  systems side by side).
- **Every number checked against the three papers on disk, 2026-09-15.**
  Findings, precise, because this batch had real errors mixed in with real
  numbers:
  - **`mem0-infographic.png` and `combined-scorecard-infographic.png`**:
    the 91% latency reduction, >90% token savings, and "26% higher
    accuracy" headline claims are accurate (Mem0's own Table 2, verified;
    the 26% figure specifically is Mem0's J-score of 66.88% against
    OpenAI's own memory feature's 52.90%, not against Full-Context, which
    the same table shows scoring *higher*, 72.90%; both images correctly
    show 66.9%/72.9% side by side when they show that comparison at all,
    the risk is a reader conflating "beats OpenAI's memory feature" with
    "beats full-context," which it does not). **The token-cost figures are
    wrong in both images**: Mem0's real memory-token count in Table 2 is
    **1,764**, not the "~7,000" both images show; Mem0g's real count is
    **3,616**, not the "~14,000" the combined scorecard shows. Full-Context's
    26,031 tokens and 17.1s p95 latency are correctly reproduced.
  - **`combined-scorecard-infographic.png` specifically**: its Zep row
    (latency ~2.9s, J-score 66.0%) is real, but it is **not from Zep's own
    paper** (which never reports those exact figures), **it is Mem0's own
    Table 2**, which evaluated Zep on the LOCOMO benchmark as a baseline
    (Zep: 3,911 memory tokens, p95 total latency 2.926s, J-score 65.99%,
    matches). The image's **"~600,000+ tokens" for Zep, with a footnote
    blaming "caching full abstractive summaries at every node," has no
    source in any of the three papers and appears fabricated.** The SeCom
    row (3,700 tokens, 71.6%) is accurate but comes from a **third,
    separate benchmark and metric** (SeCom's own LOCOMO run, GPT4Score, not
    Mem0's LLM-as-judge "J" score used in the other rows). **This table
    should not be shown as a single comparison**: it silently combines
    three different papers' own self-reported numbers on different
    benchmarks and metrics under one "Accuracy" column as if the three
    systems were evaluated head-to-head once, which none of the papers
    actually did.
  - **`zep-infographic.png`**: the LongMemEval numbers (Full-context gpt-4o
    60.2%/28.9s/115k tokens vs Zep 71.2%/2.58s/1.6k tokens, an 18.5% gain)
    are exact, checked against the paper's own Table 2. **One real error**:
    the image's closing panel says Zep "Outperforms MemGPT by 18.5%," but
    the 18.5% figure is the LongMemEval gain over a full-context baseline,
    not a comparison to MemGPT at all; the paper's only head-to-head
    against MemGPT is the separate, easier DMR benchmark, where Zep leads
    by 1.4 points (94.8% vs 93.4%), not 18.5. Fix this line before using
    the image, or drop that panel.
  - **`secom-infographic.png`**: the LOCOMO GPT4Score bars (Session-Level
    51.18, Turn-Level 57.99, SECOM 69.33) are an exact match to the paper's
    Table 1 (the MPNet-retrieval rows specifically). No issues found.
  - **`session-vs-persistent-infographic.png`**: qualitative framing plus
    the same three systems' headline numbers (26%/91%, 18.5%/90%,
    71.57/72% fewer tokens), all independently checked and accurate.
- **Decision, pending instructor input**: none of these five images are
  wired into any slide yet. `zep-infographic.png` and `secom-infographic.png`
  are usable as full-page slides once the MemGPT line is fixed (or cropped
  out) on the former; `mem0-infographic.png` needs its token-cost numbers
  corrected before use; `combined-scorecard-infographic.png` should not be
  used as a single table, its individual accurate rows could still inform
  separate, honestly-captioned slides but the cross-paper mashup itself is
  the problem, not any one number in it.

### Code track — not started

- **Tooling decision (confirmed with the instructor, 2026-09-15):** build
  both memory patterns from scratch, plain Python plus the shared
  `google-genai` client every other module's demo uses, no new heavy
  dependency, no Mem0/Zep SDK installed, no vector or graph database stood
  up. Same precedent as Module 3's `grounded_rag.py`. The lecture cites the
  real production systems accurately; the runnable demo builds the
  mechanism directly so students see what is inside it.
- Demo not yet written. Planned build order is in `lecture-notes.md` §3.

## Conventions for adding a new module or course

- One row per module in the status table above; update the cell, do not
  append a new table.
- `research/module-NN/` holds everything that feeds NotebookLM or the deck's
  research dive for that module, and nothing else:
  - `lecture-notes.md`, the module's full content, written before the deck
    (see the build order above).
  - The downloaded paper(s), named `<first-author>-<year>-<short-slug>.pdf`.
  - Any NotebookLM output actually saved back (a markdown summary, a
    reference PNG kept for provenance even when not embedded in the deck),
    named `<slug>-notebooklm-<summary|reference-N>.<ext>`, matching Module
    3's files.
- A NotebookLM prompt itself is delivered to the instructor in chat, not
  saved as a file, but its delivery date, its source document, and its
  topic are logged in this file's module section so a later session knows
  it already went out and does not resend a duplicate without checking
  first. Always name the source document a prompt was built from (the paper
  PDF, or `lecture-notes.md`); a NotebookLM prompt with no named source is a
  sign the source document does not exist yet, fix that first.
- An infographic that comes back from either prompt ships as its own
  full-page slide, `<img>` sized with `max-width:100%;max-height:<N>px` (not
  `.lu-figure__frame`, see Module 3's notes on why that class crops a
  non-photo image), with an honest caption: say plainly it is a visual aid
  and not a paper figure or a measured result, link the real source (the
  paper, or nothing if it is a concept infographic), and link the full-size
  image with `target="_blank"`. Verify with `scripts/audit-deck.js` before
  calling it done, per `AGENTS.md` §1 step 7, the same as any other slide.
- This file lives at the course-repo root, one per course
  (`course_data_science_for_conversational_ai/PROGRESS.md`,
  `course_knowledge_representation/PROGRESS.md` if that course adopts the
  same workflow later). A session working in a different course folder
  should create its own tracker there rather than adding sections here.
