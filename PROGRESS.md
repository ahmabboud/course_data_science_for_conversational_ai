# Progress tracker, Data Science for Conversational AI

Read this file first, before touching a module. It is the single place that
says what is done, what is in flight, and what a new session should pick up
next. Update it in the same turn as any work it describes, do not let it
drift behind the actual state of the repository.

This tracker exists because of three standing quality bars the instructor
set for every module, on top of the mechanical authoring contract in
`AGENTS.md`:

1. **Research dive**: the module's research section must build around a
   real, open-access, important paper, explained so anyone can follow it in
   about five slides. Not a summary of a summary, a real close read.
2. **Graphics**: the concept-explanation graphics must be high quality, not
   the bare CSS primitives look. Where a slide's diagram is still doing the
   minimum, it needs a better visual, produced via NotebookLM from an
   infographic-style prompt, then adapted into the slide (CSS primitives
   first, inline SVG second, per `AGENTS.md` §7).
3. **Code**: every demo script must be tested before it is called ready, and
   commented well enough that an instructor who did not write it can run and
   explain it live. The instructor runs the tests and owns readiness
   sign-off; this repository's job is to keep each demo's `README.md`
   accurate and to record the test/readiness status here.

## Division of labor

- **Paper track**: an agent searches for an important, open-access paper per
  module, downloads the PDF into `research/module-NN/`, and hands the
  instructor a NotebookLM prompt to turn it into a markdown summary or
  infographic for the concept explanation.
- **Graphics track**: no paper involved. An agent hands the instructor a
  NotebookLM prompt, keyed to the specific concept and slide that needs a
  better visual, for the instructor to run themselves.
- **Code track**: an agent keeps each demo's `README.md` current as the code
  changes, and hands the instructor a prompt for their own coding agent to
  add tests and comments to a demo script. The instructor runs the tests and
  updates the status below; an agent should not mark a module's code
  "tested" or "ready" on its own say-so.

## Status by module

| # | Title | Paper | Graphics | Code |
|---|---|---|---|---|
| 1 | Foundations and Modern Understanding | Not started | Not started | Not started |
| 2 | Agentic Dialogue Management | Not started | Not started | Not started |
| 3 | Grounded Generation | Done, see below | In progress | In progress |
| 4 | Memory | Not started | Not started | Not started |
| 5 | Evaluation and Responsible Deployment | Not started | Not started | Not started |

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

## Conventions for adding a new module or course

- One row per module in the status table above; update the cell, do not
  append a new table.
- `research/module-NN/` holds that module's downloaded paper(s) plus nothing
  else. Name files `<first-author>-<year>-<short-slug>.pdf`.
- A NotebookLM prompt is delivered to the instructor in chat, not saved as a
  file, but its delivery date and topic are logged in this file's module
  section so a later session knows it already went out and does not resend
  a duplicate without checking first.
- This file lives at the course-repo root, one per course
  (`course_data_science_for_conversational_ai/PROGRESS.md`,
  `course_knowledge_representation/PROGRESS.md` if that course adopts the
  same three-point workflow later). A session working in a different course
  folder should create its own tracker there rather than adding sections
  here.
