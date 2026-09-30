# Progress tracker, Data Science for Conversational AI

Read this file first, before touching a module. It is the single place that
says what is done, what is in flight, and what a new session should pick up
next. Update it in the same turn as any work it describes, do not let it
drift behind the actual state of the repository.

## Start here (updated 2026-09-30)

### 1. Before you do anything

1. **Load the `lu-lecture-builder` skill** if your environment has it. It
   covers this deck system's known failure modes and the verification
   discipline. Where it disagrees with `AGENTS.md`, `AGENTS.md` wins.
2. **Sync:** `git fetch origin`, `git status`,
   `git log --oneline origin/main..HEAD` (local, not pushed) and
   `git log --oneline HEAD..origin/main` (pushed from elsewhere). If the
   working tree has changes you did not make, stop and ask.
3. **Read, in this order:** this section; `AGENTS.md` in full, especially
   **§2c** (teaching standard), **§7 route 0** (flow animations), **§12**
   (depth bar) and §2b (measurement traps); then the detail section below
   for the module you are touching.
4. **Commits:** author is the repo's configured user (Ahmad Abboud). No
   `Co-Authored-By` or any AI attribution line. **Do not push without the
   instructor's go-ahead**; pushing publishes to GitHub Pages.

### 2. Where to continue

As of 2026-09-30, **2 commits are local and not pushed** (`f8427d8`
Module 3 layout fixes, `5f9947f` the flow-animation port, the §2c standard,
and two Module 1 prototypes). Ask the instructor before pushing.

**Waiting on the instructor (ask first, do not start without an answer):**

- **A. DECIDED 2026-09-30, approved by the instructor: use the Module 1 slide 6 "One LLM call, step by step" style (animated `.lu-flow` in a `.lu-walk`) and apply it to all the other lectures.** Not a question any more. Prototypes: Module 1 slides "One LLM
  call, step by step" and "Constrained decoding, token by token". If
  approved, that is the pattern for every module; if not, record what they
  want changed here and in `AGENTS.md` §7 before building more.
- **B. The outdated lab slides.** Module 1's lab slides (and the labs in
  Modules 2 to 5) still teach the old one-shared-agent project ("Issue 1",
  `agent/understanding.py`, "the same agent you defend in Module 6"). Ask:
  reword them as general practice exercises (a pair writes a schema and
  three test sentences for any domain, in a scratch notebook), or redesign
  each lab around the team's own paper topic?
- **C. Module 3 review.** Its four redrawn diagrams and three new slides
  (see Module 3's "Deck track" below) are built and verified but not yet
  reviewed.

**Then, in this order:**

1. **Finish Module 1 against §2c** (full findings in "Module 1 ...
   Teaching-standard audit, 2026-09-30" below):
   - New visual slides for the missing prerequisites: JSON and JSON Schema
     (real `type`/`properties`/`required`, not the current pseudo-code;
     define required and optional); the real API call from
     `demos/module-01/hook_demo.ipynb` (`client.interactions.create` with
     `response_format`); classical NLU (intent classifier plus slot tagger)
     next to one LLM call, as a flow; function calling as an animated flow
     (model picks a function and its arguments, your code runs it, the
     result goes back); Gorilla's method as a flow, with fine-tuning,
     zero-shot, AST, retriever and RLHF defined.
   - Replace the pseudo-code schema on "The schema is the whole contract"
     and the lab walkthrough with real JSON Schema.
   - Fix the six overflowing slides and `m1-q1`'s answered state (list in
     the Module 1 audit below); split slides rather than shrink them.
   - Plain-English pass on every slide's visible text and captions.
   - Apply decision B to the lab slides.
   - Rebalance `data-minutes` (keep 180 unless the instructor agrees
     otherwise) and update the slide count on `index.html`.
2. **Run the same §2c audit on Modules 2, 3, 4, 5**, one at a time: write
   the findings into that module's detail section first, show the
   instructor, then build. Module 3 has already had its layout fixed but
   not its §2c pass.
3. **Other open items** (details in each module's section): Module 3
   `lecture-notes.md` never written and `grounded_rag.py` has no tests;
   Module 4's five NotebookLM images have number errors and none are in
   the deck; Module 5's PII-pipeline infographic not decided; Modules 1, 2,
   4 and 5 show "Correct. Correct:" in some MCQ feedback (the runtime
   already adds "Correct.", so drop it from `data-fb-correct`);
   `design-system.html` has no live `.lu-flow` example yet (`AGENTS.md`
   §11 says it must); the handout prints 38 pages for Module 1's 35
   slides, so find the slides that spill onto a second page.

### 3. How to audit and rebuild a module (the §2c method)

Walk every slide and write findings under these headings, by `data-label`
(never by slide number, numbers drift):

- **Missing prerequisites.** For each term or idea a slide uses, ask: did
  an earlier slide or module teach it? Students are MSc level but many have
  never called an LLM from code. Ideas that have been missing so far: what
  one LLM call is (prompt in, text out, no memory), tokens, decoding, JSON
  and JSON Schema, the real API code, function calling, embeddings, fine-
  tuning, zero-shot, AST, RLHF, F1, and the names of datasets and hubs. A
  pop-up definition (`.lu-term`) is not enough on its own, a printed
  handout never shows it. Put the definition visibly on the slide, in
  **bold**, in one plain sentence, usually in a `.lu-callout--concept`
  labelled "Definition" or in the walkthrough caption.
- **Visuals.** Every concept slide should lead with a picture. Anything
  that moves (a request, state, tokens, a tool call, a retrieval pipeline)
  becomes an animated `.lu-flow` inside a `.lu-walk`. Anything that does
  not move can be a static flow, a table or a comparison. Mix picture
  types across a deck.
- **Language.** Students are not native English speakers. Short sentences,
  common words, no idioms. Words and phrases already found and to avoid:
  "bolted onto", "fair game", "the receipts", "rhyme with", "house style",
  "live with it", "land it", "strawman", "punctuation" (meaning a short
  slide). Headings on one line where possible. Name every acronym the
  first time.
- **Render bugs.** Audit script results, plus the answered MCQ state (see
  4 below).
- **Stale content.** Anything describing the old project model, and any
  claim about another repo (check `dsca-team-template` itself).

Adding slides is allowed (instructor, 2026-09-30). Split a crowded slide
rather than shrinking text, and move cut detail into the speaker notes.

### 4. How to build a flow animation (lessons from the Module 1 prototypes)

- Markup: copy "One LLM call, step by step" in `lectures/dsca-module-01.html`.
  One `<script type="application/json" class="lu-flow__spec">` inside
  `.lu-flow`, then one empty `<div data-walk-step="N" data-caption-short
  data-caption>` per step, all inside `.lu-walk__view`. Add
  `<script src="../assets/lu-flow.js?v=1.2.1" defer></script>` after
  `lu-deck.js` on any deck that uses it. The spec format is documented in
  the header of `assets/lu-flow.js`.
- Kinds (colour = meaning): `user` green, `model` plum, `code` blue,
  `tool` teal, `data` grey mono. States: `active` (ring), `inferred`
  (amber dashed, use for "new" or "picked"), `impossible` (red, use for
  "blocked" or "invalid"). Rename the badge text with `"flags"` and the
  legend entries with `"legend": {kind-or-state: "label"}`, so KR's words
  ("Inferred", "Impossible") never show up on a DSCA slide.
- **Space budget.** The slide body is 652px. A walk's step bar takes about
  66px, the legend about 40px (set `"legend": false` if the node labels
  already say what each colour is), the eyebrow plus a one-line h2 about
  100px with gaps. A flow taller than the walk view is clipped, not
  scaled. With a definition callout below, keep the spec height at about
  290. Measure `.lu-walk__view` against `.lu-flow`'s height.
- **Labels.** Edge labels are mono, about 12px per character, centred on
  the edge. Leave a gap between two nodes of at least the label's width
  plus 20px, or drop the label and say it in the caption. `data` nodes use
  a mono font, so make them wider than you think.
- A node's label cannot change between steps. Use a label that is true at
  every step (for example "State {party_size, day, time}", not a value
  that changes).
- Print shows the diagram's last step, but the caption shown is step 1;
  write step 1's caption so it still reads sensibly under the full diagram.

### 5. How to verify (every deck you touch, before calling it done)

1. **Serve locally.** `LebUniv/.claude/launch.json` defines `dsca-course`
   (this repo on port 8765) and `kr-course` (the Knowledge Representation
   repo on 8766, useful for looking at its animations). Otherwise run
   `python3 -m http.server 8765` in this repo's root.
2. Open the deck with a `?cb=<random>` cache-buster and clear saved state:
   `Object.keys(localStorage).filter(k=>k.startsWith('lu:')).forEach(k=>localStorage.removeItem(k))`,
   then reload. Study mode persists across reloads; make sure it is off.
3. **After any change in `assets/`, bump the version query** (`lu.css?v=`)
   in every HTML file and in `sw.js`. The service worker serves the old
   stylesheet otherwise: the first flow prototype rendered as black boxes
   for exactly this reason.
4. Run `scripts/audit-deck.js` in the console (fetch it and `eval` it).
5. **Answered MCQs.** The audit does not open the feedback box. For every
   option of every MCQ, load a fresh copy of the deck (a hidden iframe
   works), click the option, and measure the slide.
6. **Click everything**: every node popover, every walkthrough step with
   its Next button (measure at each step), every reveal, study mode (`S`).
7. **Handout:** `scripts/print-handout.sh lectures/<deck>.html <out-dir>
   8765 3,4,7` prints the handout with headless Chrome in the Handout
   button's own state and renders the listed pages to PNG for checking.
8. Structural: tags balanced, one notes template per slide, no em or en
   dashes, unique `data-qid`s, `data-minutes` per section reconciled.

### 6. Settled decisions (do not reopen without the instructor)

- Project model: paper extension (`PROJECT-REDESIGN.md`), not the old
  continuous agent.
- Provider: Gemini for every demo, for its free tier; say so honestly.
- `lu-flow` is the diagram and animation standard for new work; do not
  hand-position new `.lu-board` diagrams.
- Students are not native English speakers; plain English always.
- More slides are fine if a concept needs them.

---

**Read `PROJECT-REDESIGN.md` next, before this file's own contents below.**
Decided 2026-09-17: the continuous-agent project (one team, one domain, one
agent grown across five required GitHub issues) is being fully replaced by
a paper-extension project (each team picks one topic and one paper, and
produces a novel extension of it). Most of what this file describes below
(the per-module "Issue N" deliverables, the old capstone rubric, the old
Module 6 cross-module Q&A mechanic) reflects the design being replaced, not
the current target. Treat any conflict between this file and
`PROJECT-REDESIGN.md` as this file being the one that has not caught up
yet, and update it, rather than assuming the redesign doc is wrong.

## Project redesign, the seven-item build list

`PROJECT-REDESIGN.md`'s own "Still to build" section lists seven items.
Tracked here so a session does not have to cross-reference two files to
see what is left:

1. Fill the research-dive gap in Modules 1 and 2. **Done**, see Module 1
   and Module 2's own "Paper track and research dive" sections below.
2. Curate the paper-and-repo menu. **Done**, 2026-09-17,
   `research/PROJECT-PAPER-MENU.md`, thirteen papers across the five
   topics, each with a verified repo link and a compute/cost note.
3. Rewrite Module 1's kickoff to present the five topics, the menu, and
   the idea-pitch step. **Done**, see Module 1's own detail section below
   (the 2026-09-17 restructure), now also linking the menu file directly
   from the kickoff slide's visible text and speaker notes.
4. Rewrite the syllabus's Continuous Project, Assessment, and rubric
   sections. **Done**, per this file's earlier commit history (task #74).
5. Rebuild `dsca-team-template`'s issue templates for idea-pitch,
   baseline, extension, and report/slides. **Done**, 2026-09-17, commit
   `b76e968` in the separate `dsca-team-template` repository: the old
   `agent/` five-capability stub package and its five module issue
   templates are gone, replaced by `baseline/`, `extension/`,
   `report/REPORT.md`, `slides/README.md`, and four issue templates
   (idea-pitch, baseline-reproduction, extension, report-and-slides).
   `README.md`, `CONTRIBUTING.md`, `.env.example`, `requirements.txt`,
   and `scripts/verify_setup.py` were also rewritten so they no longer
   assume every team runs the same stack. See `PROJECT-REDESIGN.md`'s own
   item 5 for the full detail.
6. Rebuild Module 6: segment minutes, scoring sheet, defense-day
   materials. **Done**, 2026-09-17: `module-06-defense/DEFENSE-DAY.md`
   (the instructor's run-of-show) and `module-06-defense/scoring-sheet.xlsx`
   (a fillable schedule and a four-criterion, 100-point scoring sheet with
   band descriptors, zero formula errors on recalculation). The syllabus
   docx's Session 6 entry, Time Allocation table, Course Structure table,
   and per-team defense table were all brought in line with the
   paper-extension model. A real discovery along the way: the syllabus's
   own cohort size (12 to 21 participants, 6 to 7 teams) does not match
   `PROJECT-REDESIGN.md`'s illustrative "24 students, 8 teams" example, so
   both documents now treat the team count as variable and Module 6's
   timing as flexible (180-minute base, up to 1 more hour if the actual
   team count needs it) rather than reconciled to one fixed total, per
   the instructor's own direction.
7. Update `PROGRESS.md`, `index.html`, `README.md`, and the syllabus's
   remaining stale sections, so a new session sees one consistent model
   everywhere. **Done**, 2026-09-17:
   - `index.html`: the "Five modules, one project" summary paragraph and
     the Module 6 card rewritten for the paper-extension model; Modules
     1 through 3's slide counts corrected to the decks' real current
     counts (33, 31, 31; Modules 4 and 5 were already correct at 24 and
     28).
   - `README.md`: "The course in one paragraph" rewritten, the module
     status table changed from "To build" to "Built" for Modules 1
     through 5, the Repository file listing extended to cover
     `research/PROJECT-PAPER-MENU.md`, `assets/infographics/module-NN/`,
     `module-06-defense/`, and `PROJECT-REDESIGN.md`, and the
     "Before teaching from it" note about team repositories corrected to
     name `dsca-team-template` and "baseline reproduction and novel
     extension" instead of "the agents students build."
   - The syllabus docx's Course Description (Section 1), Learning
     Outcomes (Section 2, outcomes 8 and 9), and Sessions 1 through 5's
     own Objective, Deliverable, and per-segment table content (Section
     8) were rewritten to drop the old continuous-agent framing
     ("the thing you are building in week one is the thing you defend,"
     "Issue 1 merged... a working structured-extraction endpoint," "Issue
     N checkpoint," and so on). Verified by rendering to PDF and reading
     every affected page, and validated structurally (paragraph count
     unchanged, all checks passed).

**Known gap, found while doing this pass, still not fixed:** Sessions 2
through 5's own "Hands-on lab" table cells in the syllabus (and possibly
the corresponding slides in `dsca-module-02.html` through
`dsca-module-05.html` themselves, not checked here) still frame the lab
exercise as building toward "the team's agent" as a single cumulative
system (for example, "Add persistent memory to the team's agent so it
recognizes a returning user," "Build a multi-turn regression harness for
the team's own agent"). Whether these should become explicitly
topic-agnostic practice exercises (parallel to how Module 1's own lab
was just reworded, see the Session 1 detail above), or whether the labs
themselves need a real content redesign so a team whose own project
topic is Extraction still gets something useful out of Module 4's memory
lab, is a real pedagogical decision, not a wording fix, and needs the
instructor's input before a future session touches it.

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
| 1 | Foundations and Modern Understanding | Predates lecture-notes rule, slides came first; research-dive notes added 2026-09-17, see detail | Done (Gorilla, arXiv:2305.15334), see detail | Research infographic done; §2c teaching-standard audit 2026-09-30 found gaps, two animated prototypes awaiting review | Not started |
| 2 | Agentic Dialogue Management | Predates lecture-notes rule, slides came first; research-dive notes added 2026-09-17, see detail | Done (Helping Customers in Distress, arXiv:2605.16268), see detail | Done, agent-built interactive infographic, see detail | Not started |
| 3 | Grounded Generation | Not written (predates this rule, slides came first) | Done, see below | In progress; deck layout debt fixed 2026-09-30, awaiting review | In progress |
| 4 | Memory | Done, see below | Done, see below | In progress | Done, see below |
| 5 | Evaluation and Responsible Deployment | Done, see below | Done (five sources, not downloaded as PDFs), see below | 3 of 4 papers done, see below | Done, see below |

Module 6 has no lecture deck (live defense session), so it carries no row
here; see `README.md`.

## Module 1, Foundations and Modern Understanding, detail

Both decks predate the module build order above (they were the first two
built, slide-by-slide against the syllabus row directly, no
`lecture-notes.md` and no research/paper track ever existed for them, same
situation as Module 3's own "predates this rule" note). This section
records a depth-bar audit run on 2026-09-16, once all five other modules
existed and the instructor confirmed it was time to look back at Modules 1
and 2, not a rebuild.

### Depth-bar audit, 2026-09-16

- **Method:** every core-concept slide checked against `AGENTS.md` §12's
  six-row bar (formalism where the field has one, a black-box call opened
  at least once, cost stated not implied, a named alternative and why not,
  the metric the field actually uses, a critical read of a cited paper),
  applied only to slides the bar actually governs (not dividers, check
  questions, or lab briefs).
- **Row 6 (cited paper, read critically) does not apply to this module.**
  Confirmed by reading the syllabus docx directly: Session 1's reading line
  is "AI Engineering, structured output and function calling" plus an AI
  Agents in LangGraph course, and it has no Research dive segment at all.
  There is no paper for this module to cite, so this row is noted as
  structurally absent, not force-filled with an unrelated citation.
- **Two genuine gaps found and fixed** (rows 3 and 4, cost and named
  alternative):
  - Slide "Why classifiers and taggers are replaced": added the labeled-data
    cost classical intent classifiers actually paid, and the metric
    contrast (intent accuracy / slot F1 versus schema-validated exact-match
    for structured output), where the slide previously only said "editing a
    schema, not collecting labeled data" with no number or named metric
    behind it.
  - Slide "The LLM API landscape": added the real named alternative (OpenAI
    function calling, Anthropic tool use both do the same structural,
    decode-time enforcement) and the actual, honest reason this course
    standardizes on Gemini (free-tier generosity for a classroom, not a
    technical-superiority claim), where previously only one provider was
    shown with no acknowledgment that alternatives exist.
- **Minutes:** both new callouts absorbed by trimming two other Lecture-
  section slides ("Walkthrough: the correction becomes JSON,"
  "Designing for evaluation from day one"), keeping the Lecture section's
  existing total (52 minutes) exactly unchanged. Total deck minutes still
  180, slide count unchanged at 28.
- **Known pre-existing drift, not touched:** this deck's Lecture/Wrap split
  is 52/16, not the syllabus's own 50/20. This predates the current
  session's edits (confirmed the untouched `data-minutes` values summed
  identically before and after this audit's additions) and is out of scope
  for a depth-bar pass specifically; flagged here for a future session that
  wants to reconcile it, not fixed unilaterally.
- **Verified:** tag-balanced, zero em/en dashes, MCQ qids `m1-q1`/`m1-q2`
  unique, 28 slides. Committed together with Module 2's fixes, commit
  `ba77cce`.

### Paper track and research dive, added 2026-09-17

- **Why now, contradicting the 2026-09-16 audit's own note above:** that
  audit correctly found the syllabus itself names no research dive or
  paper for this module. The paper-extension project redesign
  (`PROJECT-REDESIGN.md`) changed the requirement: Extraction is now one
  of the five project topics, and every topic needs a real research-dive
  paper both for teaching parity with Modules 3-5 and as the entry point
  into that topic's paper menu (task tracked as "fill research-section
  gaps in Modules 1 and 2"). This is a deliberate addition, not a fix to
  a prior mistake.
- **Paper:** Patil, Zhang, Wang & Gonzalez (2023), "Gorilla: Large
  Language Model Connected with Massive APIs," UC Berkeley, arXiv:2305.15334,
  CC BY 4.0. Chosen (over ToolLLM) and confirmed with the instructor
  directly: canonical, has a real public repo and dataset (APIBench),
  and its central finding, that grounding a call in real documentation
  beats memorization, is the same lesson this module's own
  schema-enforcement slides already teach with one example, just
  measured at the scale of 1,645 real APIs.
- **Not downloaded as a local PDF**, same standing sandbox limitation as
  every module since Module 5 (no outbound fetch to arXiv's PDF
  endpoint). Verified against the arXiv HTML rendering
  (`arxiv.org/html/2305.15334v1`), fetched and read in full, no
  truncation (a much shorter paper than tau-bench or tau2-bench).
- **Lecture notes:** `research/module-01/lecture-notes.md`, scoped to the
  research dive only, not a retroactive full-module rewrite (see the
  file's own scope note). Covers the hallucination problem, APIBench's
  construction, AST sub-tree matching as the verification method,
  retriever-aware fine-tuning, the full results (accuracy and
  hallucination-rate tables), and the paper's own stated limits,
  including its honest unresolved finding that GPT-3.5 hallucinates less
  than GPT-4 in their tests.
- **Deck:** five new slides in `lectures/dsca-module-01.html`, a new
  "Research dive" section (12 minutes) placed after the Lecture section
  and before the Kickoff section: a divider, the problem (APIBench,
  GPT-4's 78.65% TensorHub hallucination rate), the method
  (retriever-aware fine-tuning), the results (Gorilla beats GPT-4 by
  20.43 points overall, cuts TensorHub hallucination from 78.65% to
  5.40%), and the limits. Minutes rebalanced from Lecture's prior 52 to
  40 (nine slides trimmed by 1-3 minutes each, teaching content
  untouched, only pacing) to fund the new section; total deck minutes
  still 180, slide count now 33. Linked from the "Before Module 2" reading
  callout as this module's own research-dive reading.
- **Verified:** tag-balanced, zero em/en dashes, MCQ qids `m1-q1`/`m1-q2`
  unique (unchanged, no new check questions added), 33 slides, `data-minutes`
  reconciling to Opening 2 / Hook 20 / Lecture 40 / Research dive 12 /
  Kickoff 20 / Lab kickoff 70 / Wrap 16 = 180.

### Graphics track: done

- **Shipped 2026-09-17:** `assets/infographics/module-01/gorilla.html`, an
  agent-built (not NotebookLM, not Clearpaper template), self-contained,
  interactive infographic, built at the instructor's own direction after
  they asked whether an agent could extract the paper's real figures and
  build the page itself, with the explicit steer to skip the shared
  design system and favor a click-to-reveal, low-noise interactive layout
  instead. Structure: a hero stat (the 78.65% to 5.40% TensorHub
  hallucination drop), the paper's own Figure 3 pipeline diagram (real
  image, not redrawn, see below), five click-to-expand pipeline-stage
  panels, four click-to-expand results stat cards, a static results
  table, and a collapsible "what this paper does not claim" section.
  Every number fact-checked against `research/module-01/lecture-notes.md`
  and, directly, against the arXiv HTML text
  (`arxiv.org/html/2305.15334v1`). Full provenance in
  `assets/infographics/module-01/README.md`.
- **Figure extraction method:** the paper's own Figure 3
  (`arxiv.org/html/2305.15334v1/llmapi.png`, CC BY 4.0) was loaded in the
  built-in browser, redrawn to a canvas, and re-exported at a small size
  (200x125px, roughly 5KB) so the resulting base64 data was short enough
  to transcribe reliably; saved to
  `assets/infographics/module-01/images/gorilla-pipeline-original-figure.jpg`
  and verified both by file type/dimensions and by visually viewing the
  decoded image, to catch any transcription error before it shipped. The
  page links out to the full-resolution original on arXiv.
- **Linked in exactly two places**, per `AGENTS.md` §7b: the "The
  problem: LLMs hallucinate API calls" slide's speaker notes in
  `lectures/dsca-module-01.html`, and the "Before Module 2" reading
  callout, both pointing to `../assets/infographics/module-01/gorilla.html`.
  Not embedded inline anywhere in the deck.

### Teaching-standard audit, 2026-09-30 (AGENTS.md §2c): findings, prototypes awaiting review

Run against the new §2c standard (visuals first, animated dataflow, plain
English for non-native speakers, no missing prerequisites, more slides
allowed). Findings, by `data-label`:

**Render bugs** (`scripts/audit-deck.js`, local, storage cleared): six
slides cut content off: "Why classifiers and taggers are replaced" 138px,
"How the enforcement actually works" 46px (68px revealed), "The LLM API
landscape" 156px (197px revealed), "Gorilla: retrieval-aware fine-tuning"
132px, "Form your team, pick your topic and paper" 15px, "Discussion and
wrap" 68px. MCQ `m1-q1` overflows 99px once answered. Not yet fixed.

**Prerequisite gaps** (ideas a slide uses that the course never teaches):
- What an LLM call is: prompt in, text out, no memory between calls.
  The whole "state is passed in" lesson depends on it.
- Tokens and decoding: "How the enforcement actually works" talks about
  tokens, sampling and zero probability with no picture of generation.
- JSON and JSON Schema: the deck's schema is pseudo-code
  (`"integer | null"`); the real call in `demos/module-01/hook_demo.ipynb`
  uses real JSON Schema (`type`, `properties`, `required`). "Required" and
  "optional" are used in the bugs table but never defined.
- The actual API call is never shown: no slide opens
  `client.interactions.create(..., response_format=...)`.
- Function calling versus structured output: defined only in popovers,
  never shown as a flow (model picks a function, your code runs it).
- Classical NLU: "intent classifier", "entity tagger", "slot",
  "sequence labeling", "F1" appear without a picture of the old pipeline.
- Research dive: fine-tuning, zero-shot, self-instruct, AST and sub-tree
  matching, retriever, RLHF, HuggingFace/TorchHub/TensorHub are used
  without definitions.

**Visuals**: apart from the five-stage pipeline, every concept slide is
text or code. No diagram for the old versus new pipeline, the call loop,
function calling, constrained decoding, or Gorilla's method.

**Plain English**: slide text uses idioms a non-native reader will
stumble on ("bolted onto", "fair game", "the receipts", "rhyme with the
example", "no house style", "live with it"). Several h1s are long
two-line sentences.

**Stale project model**: the lab slides still teach the old
continuous-agent project: "Issue 1", `agent/understanding.py`'s
`extract()`, "Issue 1 merged", `dialogue.py`, a "memory-service key", and
"the same agent they defend in Module 6" (title notes, "The five stages",
"Lab kickoff · what you build", "Documenting the decision for the PR",
"Discussion and wrap"). None of these exist in the rebuilt
`dsca-team-template`. This is the same open decision as the Modules 2 to 5
labs (see the known gap at the top of this file): reword as a practice
exercise, or redesign.

**Prototypes built 2026-09-30, awaiting the instructor's review** (not
yet approved as the style for the rest of the rebuild):
- `assets/lu-flow.js` ported from the Knowledge Representation course,
  with this course's own kinds (`user`, `model`, `code`, `tool`, `data`),
  plus its CSS (section 8d), colour tokens, and the walkthrough
  `overflow:hidden` fix. Asset version bumped to `lu.css?v=1.3.0`
  everywhere; `lu-flow.js` added to `sw.js`'s cache list.
- New slide "One LLM call, step by step" (4 steps: code gets the line and
  the state, one prompt to the LLM, the LLM writes JSON, code parses and
  saves the new state), with a visible definition box.
- New slide "Constrained decoding, token by token" (4 steps: text so far,
  candidates go to the schema check, three bad tokens blocked, the comma
  picked).
- Both measured at 0px overflow at every step; minutes rebalanced to keep
  the Lecture section at 40 and the deck at 180. Deck is now 35 slides.

## Module 2, Agentic Dialogue Management, detail

Same predates-the-build-order situation as Module 1 (no `lecture-notes.md`,
no paper track, slide-by-slide against the syllabus row). Audited in the
same pass as Module 1, 2026-09-16.

### Depth-bar audit, 2026-09-16

- **Row 6 (cited paper, read critically) does not apply to this module
  either.** Confirmed via the syllabus docx: Session 2 reads "AI Agents in
  LangGraph, persistence and human-in-the-loop" and "Anthropic, Building
  Effective Agents, the routing pattern," an engineering blog post, not an
  academic paper, and there is no Research dive segment in this module's
  row. Noted as structurally absent, not forced.
- **Three genuine gaps found and fixed** (rows 3 and 4):
  - Slide "The raw agent loop, with nothing hidden": added the O(n^2)
    total-token-cost consequence of resending the whole messages array on
    every call across an n-turn conversation, derived directly from a fact
    already stated on the slide (every call resends the full array), not a
    new external statistic. Deliberately foreshadows Module 4's
    compaction lecture.
  - Slide "Chain-of-thought for tool selection": added the named,
    cheaper alternative (skip straight to a tool call, no reasoning field)
    and the real accuracy/cost tradeoff against it, where the slide
    previously presented chain-of-thought as the only option.
  - Slide "The one multi-agent pattern this course teaches: routing and
    escalation": replaced a course-scoping justification ("out of scope
    for this course") with the actual technical reason general multi-agent
    orchestration is avoided (coordination overhead, emergent failure
    modes), sourced from this module's own assigned reading (Anthropic,
    "Building Effective Agents") rather than scope alone.
- **Minutes:** absorbed by trimming three other Lecture-section slides
  ("Check: what LangGraph actually adds," "Walkthrough: one tool call
  through MCP," "Walkthrough: a turn that gets escalated"), keeping the
  Lecture section at exactly the syllabus's own 50 minutes (this deck's
  section totals already matched the syllabus before this audit, unlike
  Module 1). Total deck minutes still 180, slide count unchanged at 26.
- **Verified:** tag-balanced, zero em/en dashes, MCQ qids `m2-q1`/`m2-q2`
  unique, 26 slides. Committed together with Module 1's fixes, commit
  `ba77cce`.

### Paper track and research dive, added 2026-09-17

- **Why now:** same reasoning as Module 1's own paper track above.
  Dialogue is one of the five paper-extension project topics, and this
  module's own scope (routing and escalation, deliberately the one
  multi-agent pattern taught) needed a real research-dive paper to match.
- **Paper:** Atreya, Wanger, Batra, Hankache, Iglesias Jr, Sinclair,
  Pelosio, McMillan, Cowan & Khraishi (2026), "Helping Customers in
  Distress: An LLM-powered Agent that Converses, Probes, and Routes,"
  arXiv:2605.16268, CC BY 4.0, `cs.HC`. Chosen (over MultiWOZ) and
  confirmed with the instructor directly: a recent, directly on-topic
  production deployment of this module's own router-plus-escalation
  pattern, at a bank, on fraud/scam/dispute triage, with real measured
  accuracy, handoff precision/recall, and guardrail numbers.
- **Fetched in full**, no truncation, a short paper: the arXiv HTML
  rendering (`arxiv.org/html/2605.16268v1`) returned every section,
  unlike the longer Module 5 papers. Not downloaded as a local PDF, same
  standing sandbox limitation.
- **Lecture notes:** `research/module-02/lecture-notes.md`, scoped to the
  research dive only, same convention as Module 1's new notes. Covers
  the triage problem, the three-agent architecture (triage, handoff,
  guardrails), the digital-twin-plus-SME evaluation method, the full
  results (accuracy gains across five LLMs, handoff precision/recall,
  guardrail accuracy), and the paper's own stated limits, including the
  gap between its synthetic-testing and SME-tested accuracy figures.
- **Deck:** five new slides in `lectures/dsca-module-02.html`, a new
  "Research dive" section (12 minutes) placed after the Lecture section
  and before the Hands-on lab section: a divider, the problem (millions
  of fraud/scam/dispute reports, manual triage), the architecture
  (triage agent, handoff agent, guardrail agents as three separate
  jobs), the evaluation (digital twins plus SME and LLM-judge review,
  with the objective-versus-subjective agreement gap named explicitly),
  and the results (up to +30.6% accuracy gain, >90% handoff precision
  and recall, 96-98% guardrail accuracy). Minutes rebalanced from
  Lecture's prior 50 to 38 (nine slides trimmed by 1-3 minutes each,
  teaching content untouched, only pacing) to fund the new section;
  total deck minutes still 180, slide count now 31. Linked from the
  "Before Module 3" reading callout as this module's own research-dive
  reading.
- **Verified:** tag-balanced, zero em/en dashes, MCQ qids `m2-q1`/`m2-q2`
  unique (unchanged, no new check questions added), 31 slides,
  `data-minutes` reconciling to Opening 2 / Lecture 38 / Research dive
  12 / Hands-on lab 100 / Wrap 28 = 180.

### Graphics track: done

- **Shipped 2026-09-17:**
  `assets/infographics/module-02/helping-customers-in-distress.html`, an
  agent-built (not NotebookLM, not Clearpaper template), self-contained,
  interactive infographic, same instruction and same reasoning as Module
  1's (see that module's Graphics track entry above). Structure: a hero
  stat (the +30.6% best synthetic accuracy gain), the paper's own Figure
  1 triage-and-handoff architecture diagram (real image, not redrawn, see
  below), five click-to-expand architecture-role panels (Triage Agent,
  Handoff agent, Guardrail agents, Digital twins, Human plus automated
  evaluation), four click-to-expand results stat cards, a static results
  table across five LLMs with confidence intervals, and a collapsible
  limits section that names the gap between the synthetic-testing figure
  (+30.6%) and the SME-tested figure (+16.0%) directly rather than
  smoothing over it. Every number fact-checked against
  `research/module-02/lecture-notes.md` and, directly, against the arXiv
  HTML text (`arxiv.org/html/2605.16268v1`). Full provenance in
  `assets/infographics/module-02/README.md`.
- **Figure extraction method:** the paper's own Figure 1
  (`arxiv.org/html/2605.16268v1/figures/workflow_triage4.png`, CC BY 4.0)
  was loaded in the built-in browser, redrawn to a canvas, and
  re-exported at a small size (220x141px, roughly 4KB), then saved to
  `assets/infographics/module-02/images/triage-workflow-original-figure.jpg`
  and verified both by file type/dimensions and by visually viewing the
  decoded image. The page links out to the full-resolution original on
  arXiv.
- **Linked in exactly two places**, per `AGENTS.md` §7b: the "The
  problem: triage is slow, manual, and easy to misroute" slide's speaker
  notes in `lectures/dsca-module-02.html`, and the "Before Module 3"
  reading list, both pointing to
  `../assets/infographics/module-02/helping-customers-in-distress.html`.
  Not embedded inline anywhere in the deck.

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

### Deck track: layout debt fixed 2026-09-30, awaiting instructor review

The overflow and stray-edge debt found on 2026-09-15 is fixed. Deck is now
34 slides (was 31), 180 minutes, section budgets unchanged (Opening 2,
Lecture 37, Research dive 22, Hands-on lab 86, Wrap 33). Not yet reviewed
by the instructor; a redraw on this deck was rejected once before (see the
Graphics track above), so get a look at the four redrawn boards before
calling the deck done.

What changed, by `data-label` (slide numbers drift, labels do not):

- **Root cause of most of the overflow:** every `.lu-board` was
  `width:100%` plus the default `aspect-ratio:16/7`, so it rendered 634px
  tall inside a 652px slide body. The four boards ("Hybrid search",
  "Reranking", "Citation and the refusal path", "The idea: skip
  retrieval") now have an explicit height (290 to 340px),
  `aspect-ratio:auto`, and `flex:none`. `flex:none` matters: without it
  study mode's legend squashes a fixed-height board to a sliver instead
  of clipping. Each board's viewBox now matches its rendered aspect ratio,
  and every edge path was recomputed from the measured node boxes, so the
  six stray endpoints are gone. "The idea" board's long RAG label was
  shortened to "RAG: retrieve + generate, per query" and moved right of
  its node.
- **Three reveals became their own slides**, because their revealed
  content could never fit under a diagram:
  "Under the hood: what each lane actually computes" (new, after "Hybrid
  search", BM25 and cosine formulas plus the HNSW/IVF callout; minutes
  8 split 5 + 3), "Why reranking is a different cost, in Big-O terms"
  (new, after "Reranking", a bi-encoder versus cross-encoder table;
  6 split 4 + 2), and "A metric worth naming: what BERTScore can and
  cannot tell you" (new, after "The experiment", a table of BERTScore,
  Recall@k, MRR and nDCG@k with how each is computed; 5 split 3 + 2).
  Nothing taught was dropped; see each new slide's speaker notes.
- **Both MCQs cut to three options**, because the answered state (with
  its feedback box, which `scripts/audit-deck.js` does not open)
  overflowed by 130px (`m3-q1`) and 54px (`m3-q2`). `m3-q1` lost "a
  larger context window" and its companion callout, and its correct answer
  is now `a`. `m3-q2` lost "silently retry the pipeline", and its
  rationales were shortened to one line. The cut options and the long
  rationales are in each slide's speaker notes. The duplicated
  "Correct. Correct:" feedback on `m3-q2` is fixed.
- **"The limits"** and **"Likely bugs"**: wider left column
  (`lu-split--wide-left`), shorter text, cut detail moved to notes.
- `index.html` Module 3 card: 31 to 34 slides.

Verified 2026-09-30, locally (`python3 -m http.server` plus the browser
pane), cache-busted, `lu:` storage cleared:

- `scripts/audit-deck.js`: zero failures for overflow (at rest and
  revealed), hidden leaks, grid escapes, stray characters, collisions and
  edges. `tinyText` still lists 8 elements, the same 8 as before these
  edits: the title slide's lockup unit (19px) and the `<kbd>` shortcut
  chips on the title and self-check slides (13px). These are styled in
  shared `assets/lu.css` for every deck, not by this deck.
- Clicked: every diagram node popover (11, none off-slide), every
  walkthrough through every step with its Next button (six walkthroughs,
  0px overflow at every step), the one remaining reveal, and every option
  of both MCQs, each from a fresh unanswered load (all six grade correctly
  and fit).
- Handout printed to PDF with headless Chrome, with the deck's own study
  mode switched on, the same state the Handout button produces. Changed
  pages read back: nothing clipped.
- Structural: tags balanced, 34 slides with 34 notes templates, no em or
  en dashes, `data-qid`s unique.

Still open on this deck:

- **Study mode on screen** clips the bottom of the node legend on the four
  board slides (171 to 279px). This is the known gap in `AGENTS.md` §8
  (study mode does not scroll yet), not new debt; the handout, which is
  the conforming alternative, prints them in full.
- Not checked: presenter view (`P`) and the timer (`T`).
- Found in passing, not fixed: Modules 1, 2, 4 and 5 each have one or two
  `data-fb-correct` strings starting with "Correct", which the runtime
  already prefixes, so students see "Correct. Correct:".

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

### Code track: done (superseded an earlier tooling decision)

- **Original tooling decision (2026-09-15, superseded):** build both
  memory patterns from scratch, no Mem0/Zep SDK installed, same precedent
  as Module 3's `grounded_rag.py`. Reversed once building started: Mem0 is
  a named course tool per the syllabus itself, so `demos/module-04/
  memory_demo.py` runs the real `mem0ai` package directly, not a
  reimplementation, matching `module-04/README.md`'s own stated reasoning.
- **Built:** `memory_demo.py` (extraction and conflict resolution, a
  second `Memory` instance standing in for a process restart, compaction,
  and a verified `forget_user()`), plus `memory_demo.ipynb`, a self-study
  companion that imports the script's own functions.
- **Fixed 2026-09-16 (was open as its own pending item):** the lecture
  deck had not caught up to a real correction the instructor made directly
  in `memory_demo.py`: current `mem0ai`'s `add()` is additive only, not
  the paper's own described similarity-triggered auto-UPDATE/DELETE/NOOP.
  Five places in `lectures/dsca-module-04.html` (slides 5, 7, 14, 16, 18)
  taught the old, automatic model, including MCQ `m4-q2`, whose correct
  answer was flatly wrong under the real, verified behavior. Corrected all
  five, added an explicit "paper versus the library you actually run"
  callout on slide 5, and rewrote `m4-q2` to test the corrected
  understanding. Commit `2c89df6`.

## Module 5, Evaluation and Responsible Deployment, detail

Planned and built 2026-09-16, following the module build order above, with
one process deviation noted in the paper track below.

### Syllabus row (Session 5, from the syllabus docx, rebalanced 2026-09-16)

- **Objective.** Decide, with evidence, whether the agent built over the
  last four modules is actually good and safe to put in front of users.
- **Segments (rebalanced this pass, previous split was Lecture 35 / Research
  dive 20 / Hands-on lab 95).** Lecture 50 min (component metrics versus
  end-to-end and trajectory-level metrics, bias probing, PII detection and
  redaction and regulation, deployment concerns); Research dive 40 min
  (tau-bench and tau2-bench, the documented blind spots of LLM-as-judge
  grading); Hands-on lab 60 min, capped firmly at the instructor's request
  (build a multi-turn regression harness, run bias and PII-leakage probes,
  produce a scorecard); Discussion and wrap 30 min (defend-rubric read
  against the team's own scorecard, Issue 5 checkpoint). Total 180.
- **Deliverable (Issue 5).** A working evaluation harness with a scripted
  regression set, plus a scorecard covering task success, bias probes, and
  PII probes for the team's own agent.
- **Reading.** *AI Engineering*, the evaluation chapter. The tau-bench and
  tau-squared-bench papers (named directly in the syllabus's own reading
  line, the two anchor papers for this module, see paper track below).
- **Rubric rows.** Evaluation rigor (15 pts): the regression harness is
  reproducible and trajectory-aware, not just final-answer accuracy, and
  the team reports its own weaknesses honestly. Ethics/privacy/safety
  (5 pts): bias probe results and PII handling are documented and
  demonstrated, not just claimed.

### Lecture-notes track: done

- **Written to:** `research/module-05/lecture-notes.md`. Covers the
  compounding-error problem and pass^k, tau2-bench's dual-control model and
  its reasoning-vs-coordination split, persona-conditioned bias in task
  performance, the PII detection-and-redaction pipeline mechanism, EU AI
  Act Article 50 versus the deferred Annex III date stated precisely,
  deployment concerns (latency budgets, cost per conversation, drift), and
  the trajectory-judge paper's full blind-spot findings, at the `AGENTS.md`
  §12 depth bar.
- **Not yet done:** instructor review and edit, same standing rule as every
  other module's lecture-notes track.

### Paper track: done, with one process deviation

- **The two anchor papers, named directly in the syllabus's own Research
  dive line and Reading line:** Yao, Shinn, Razavi & Narasimhan (2024),
  "tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World
  Domains," arXiv:2406.12045; and Barres, Dong, Ray, Si & Narasimhan
  (2025), "tau2-Bench: Evaluating Conversational Agents in a Dual-Control
  Environment," arXiv:2506.07982.
- **Two supporting citations**, not syllabus-named, added to answer the
  syllabus's own framing questions with real, verified numbers: Mohammadi
  (2026), "trajectory-judge: What Outcome-Only LLM Judges Miss on Agent
  Trajectories," arXiv:2609.00038 (single-author preprint, under review,
  cited as the only source found with concrete, ground-truth-by-
  construction numbers for the syllabus's own "how much it under-detects"
  phrase); and Cao, Sun & Yue (2026), "From Biased Chatbots to Biased
  Agents," AAAI 2026 TrustAgent Workshop, arXiv:2602.12285 (bias-probing
  mechanism and its 26.2% figure). Plus one peer-reviewed anchor for
  critical reading: Zheng et al. (2023), NeurIPS 2023 Datasets and
  Benchmarks, arXiv:2306.05685.
- **Deviation from the standard process, and why:** none of these five
  sources were downloaded as local PDFs into `research/module-05/`, unlike
  every prior module's paper track. This sandbox has no outbound fetch to
  arxiv.org's PDF endpoint (confirmed via a failed direct `curl`, and a
  `web_fetch` call that returned an oversized, unusable text dump); only
  abstract/HTML pages were reachable. The arXiv links in
  `lecture-notes.md`'s sources section are the citable source until a PDF
  copy is added by whoever has an environment that can download one.
- **First deck draft over-weighted all four sources equally** (2026-09-16):
  built with tau-bench, tau2-bench, trajectory-judge, and the persona-bias
  paper as four co-equal deep-dive papers. Corrected the same day, after the
  instructor questioned the paper count, once a direct read of the syllabus
  docx confirmed only tau-bench and tau2-bench are actually named for the
  research dive. The deck now gives those two the deepest treatment (10 and
  9 minutes respectively) and reframes trajectory-judge as supporting
  evidence (6 min) and the persona-bias paper as a compact citation (4 min).
  See commits `f2c215f` and `108d17b`.
- **NotebookLM prompts:** not sent through the usual flow. The instructor
  asked for the raw arXiv links directly, to build infographics in parallel
  with the deck rather than through a NotebookLM handoff; links were given
  in chat on 2026-09-16 (tau-bench, tau2-bench, trajectory-judge,
  persona-bias, Zheng et al.). No infographic has come back yet.

### Graphics track: three of the module's papers done, PII pipeline still open

- **Shipped 2026-09-16:** `assets/infographics/module-05/tau-bench.html`,
  `tau2-bench.html`, and `trajectory-judge.html`. Instructor-designed
  (Clearpaper template), delivered as finished HTML files and integrated
  by an agent per `AGENTS.md` §7b: fact-checked against each paper's own
  text (fetched from arXiv), linked from the corresponding research-dive
  slide's speaker notes (`tau-bench, worked through`,
  `tau-squared-bench: when the user can act too`,
  `The blind spot: what an outcome-only judge misses`) and from the
  "Before Module 6" reading slide's visible link list, never embedded
  inline. Full fact-check findings, including which specific numbers were
  confirmed against the primary source and which could not be reached in
  this pass (a sandbox page-fetch limitation, not a finding of error), are
  in `assets/infographics/module-05/README.md`. Short version:
  `trajectory-judge.html` fully verified (paper's short enough to fetch in
  full); `tau-bench.html` and `tau2-bench.html` have their headline
  figures verified but a handful of more granular numbers (tau-bench's
  per-model comparison bars and failure-cause breakdown, tau2-bench's
  step-count cliff chart) were not reachable in the fetched text and are
  flagged, not confirmed or contradicted.
- Still offered, not yet actioned: a `research/module-05/pii-pipeline-notes.md`
  brief (matching `lecture-notes.md`'s format) for the PII
  detection-and-redaction pipeline, a non-paper mechanism dense enough to
  merit its own infographic, in the same style as Module 4's four
  standalone infographics. Instructor has not yet said whether they want
  this written.

### Deck track: done

- **Built:** `lectures/dsca-module-05.html`, 28 slides. Heavy use of
  `.lu-pipeline`, `.lu-board`, `.lu-matrix`, `.lu-walk`, and `.lu-table` per
  the instructor's explicit "less reading, more expressive images and
  illustrations" instruction. Verified tag-balanced, zero em/en dashes, two
  unique MCQ `data-qid`s (`m5-q1`, `m5-q2`), and `data-minutes` reconciling
  exactly to 2 Opening / 50 Lecture / 40 Research dive / 60 Hands-on lab /
  28 Wrap = 180 (the 2-minute Opening carve-out taken from the syllabus's
  30-minute Discussion-and-wrap line, same precedent as every prior module).
  Commits `f2c215f` (initial build) and `108d17b` (two-anchor-paper
  rebalance, see paper track above).
- **Done since:** `index.html`'s Module 5 card, previously a disabled
  "Not yet built" placeholder, now links to the built deck (commit
  `4a854d4`).
- **Not yet done:** live rendering/click-through verification in an actual
  browser (this sandbox cannot serve localhost to its own browser pane,
  same standing gap as Modules 3 and 4).

### Code track: done

- **Built:** `demos/module-05/eval_harness.py`, evaluating a small,
  deliberately flaky toy order-status agent (built for this demo, not a
  reimplementation of any team's real one). Implements all four of the
  lecture's lab pieces: a scripted regression set with full trajectory
  capture and a pass^k run (`PASS_K = 3`, `FLAKE_RATE = 0.4` on the one
  tool call, seeded for reproducibility), a structured Gemini judge
  grading each trajectory against a known-correct expected outcome rather
  than the final reply alone, a bias probe (identical seed, only a
  persona cue differs), and a PII-leakage probe.
- **Reuses Module 4's memory functions rather than reimplementing them:**
  imports `close_memory`, `forget_user`, `retry_transient`, and Module 4's
  own verified `MEM0_GENERATION_MODEL`/`MEM0_EMBEDDING_MODEL` pair directly
  from `module-04/memory_demo.py`. Only `new_memory()` is redefined, with
  its own `mem0_store/` and collection name, so the two modules' demos
  share code, never on-disk state.
- **Verified 2026-09-16** with a full dry run: `mem0` and `google.genai`
  stubbed out (a fake in-memory store; a fake judge that compares the
  prompt's stated expected outcome against the fake agent's reply) and run
  as a real subprocess via `PYTHONPATH`, the same technique used to verify
  Module 4's script and notebook. Confirmed end to end: `order-shipped`
  correctly shows `pass_1: true, pass_3: false` at this seed (2 of 3
  attempts hit the stale-cache path), `order-processing` shows
  `pass_1: true, pass_3: true` (a clean control), the bias probe and PII
  probe both run and report their booleans, and the scorecard writes valid
  JSON. This checks structure and control flow, not a real model's
  judgement quality; the instructor still owns confirming that with a live
  key, same division of labor as every other module's Code track.
- **Written:** `demos/module-05/README.md` (run steps, what each part
  shows, why the toy agent is deliberately flaky). Added a
  `demos/README.md` table row, an `M05_GENERATION_MODEL` entry in
  `demos/.env.example`, a `requirements.txt` comment noting no new package
  is needed, an `eval_scorecard.json` gitignore entry, and a cross-reference
  from the deck's own "What you build today" slide (18) speaker notes back
  to this demo, matching every other module's two-way link convention.
- **Self-study notebook companion added, 2026-09-16:**
  `demos/module-05/eval_harness.ipynb`, same status and precedent as
  Module 4's `memory_demo.ipynb`, imports `eval_harness.py`'s own functions
  rather than copying them. Chosen for this module specifically because its
  four probes produce things worth inspecting inline (a full trajectory, a
  pass^1 vs pass^3 table, the bias probe's two replies side by side, the
  scorecard), not just a pass/fail line, closer to how evaluation work is
  actually read than Module 2 or 3's single-script demos. Adds one cell
  beyond a plain narrated walkthrough of the script: pulling out one
  attempt the judge actually failed and printing its real tool result and
  reply, so a "silent fault" is something a student reads, not a summary
  boolean.
  - **Executed and saved with a stubbed dry run, not a live model**, same
    technique already used to verify `eval_harness.py` itself before a live
    key was available: `mem0` and `google.genai` replaced with small
    stand-ins that parse the prompt text this file builds and return
    schema-conformant answers derived from it, exercising every cell's real
    control flow. Reproduced the intended teaching story exactly:
    `order-shipped` shows `pass_1: true, pass_3: false`, `order-processing`
    shows a clean `pass_1: true, pass_3: true`, and the PII probe passes.
    The one number this stub cannot speak to honestly is the bias probe's
    `delta_detected` (came back `False` here, since the stub judge only
    matches status words, not persona-sensitive phrasing); the notebook's
    own first cell says this explicitly and asks the instructor to rerun
    it once with a real `GOOGLE_API_KEY` before treating that specific
    result as real, same division of labor as every other module's Code
    track.
  - `demos/requirements.txt` and `demos/module-05/README.md` updated to
    reference the notebook, matching Module 4's README section.

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
