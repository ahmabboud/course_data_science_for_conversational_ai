# Project redesign: paper-extension teams replace the continuous agent

Decided 2026-09-17. This is the locked source of truth for the new course
project. Read this before touching the syllabus, any lecture module, or
`dsca-team-template`: several of those still describe the old design and
need to be brought in line with what is written here, not the other way
around.

## Why this exists

The original design (one team, one chosen domain, one agent grown across
five modules, one GitHub issue per module) has a fatal flaw for a 2026
cohort: a team can find an equivalent agent on GitHub, or ask a coding
agent to build the whole thing end to end, and never demonstrate real
understanding. The fix is a project shape that cannot be forked whole:
each team extends a specific paper with its own new idea. An idea cannot
be copy-pasted the way code can; a team still has to specify, defend, and
implement the one part that does not already exist anywhere.

## What replaces the continuous agent

Instead of building one agent with five required capabilities, each team
picks **one topic** and, inside it, **one paper**, and produces a **novel,
useful extension** of that paper, baseline reproduction included.

### The five topics

Fixed to the course's own five pillars, so each team's deep dive lines up
with material the whole cohort gets taught, at lecture depth, either way:

1. **Extraction** (Module 1's subject: structured intent and entity
   extraction, function calling).
2. **Dialogue** (Module 2's subject: agentic dialogue management,
   state, routing, escalation).
3. **Grounding** (Module 3's subject: retrieval, hybrid search,
   citation, refusal).
4. **Memory** (Module 4's subject: session and persistent memory).
5. **Evaluation** (Module 5's subject: trajectory-level evaluation,
   bias and PII probing).

### Team and paper selection

- Teams of up to 3. Cohort of 24 students means 8 teams.
- Each team picks one topic and one paper. The paper can come from the
  curated menu (see "Still to build" below) or be self-proposed, subject
  to the idea-pitch approval step below either way.
- **Multiple teams may extend the same paper.** Not a problem, not
  restricted. Two teams can converge on the same baseline and even
  similar extension ideas; that is fine.
- **A paper already taught in a lecture's own research dive is a valid
  choice**, as long as it fits the team's chosen topic (tau-bench or
  tau2-bench for Evaluation, SeCom or Mem0 or Zep/Graphiti for Memory,
  the CAG paper for Grounding, and so on). Teaching it in class does not
  disqualify it from being extended; it may make the pitch easier to
  approve quickly, since the instructor already knows the baseline well.
- **Compute and cost cap:** must run on a personal computer, or with no
  more than $20 of API spend total. This is a hard, concrete ceiling, not
  a vibe, so a self-proposed paper can be checked against it in one
  question: does it fit this box, yes or no.
- **A smoke test standing in for full-scale validation is acceptable**,
  provided the team can demonstrate, in the report and defense, that they
  understand what a full-scale validation would actually require (data
  volume, compute, time) even though they did not run it. This is
  explicitly not a penalty as long as the awareness is real and stated,
  not glossed over.

### Two guardrails against the same problem returning one level up

Extending a paper does not automatically block the newer failure mode: a
team finding someone else's already-published follow-up paper and
presenting it as their own idea.

1. **Idea-pitch approval.** Each team submits a one-paragraph pitch of
   their intended extension before doing real work on it. The instructor
   approves it. This is a light checkpoint, not a formal process, but it
   exists specifically to catch "this already exists as a published
   follow-up" before a team invests weeks in it.
2. **Related-work honesty in the report.** The final paper-style report
   must cite related follow-up work on the same baseline and explicitly
   state how the team's extension differs from it. Silence on this point
   is itself a flag.

## Deliverables, due before defense day

All three submitted to the instructor before Module 6, not walked in with
on the day:

- **Slides:** a cover slide, references slide, and **no more than 6
  content slides** in between. Content covers, in order: the baseline
  paper's problem, solution, and results, then the team's extension idea
  and results.
- **Repository:** working code for the baseline reproduction and the
  extension.
- **Paper-style report:** explains the extension, including the code and
  the results (and, if only a smoke test was run, says so plainly and
  states what full validation would require).

Submitting all three in advance is what makes the defense-day rubric
below actually gradeable: the instructor reads before the room, and asks
targeted questions live rather than judging novelty cold in real time.

## Defense day (Module 6)

- **12 minutes presenting, 12 minutes of questions, per team.** 8 teams
  is 192 minutes of defenses alone, before setup, deliberation/scoring,
  and course close. The instructor has agreed to extend Module 6's
  session length to fit this (originally a fixed 3-hour block); the exact
  new total and its internal segment minutes are decided when Module 6
  itself is rebuilt (a separate, still-open task), not fixed here. Time
  is deliberately not the constraint being protected in this document;
  the content and rubric decisions above and below are.
- **Any of the three teammates can be asked about any part**: the
  baseline paper, the extension idea, or the code. There is no
  division of "who built what" the way the old design had one person per
  module; full shared ownership is the point, and Q&A tests exactly that.

## Rubric: 100 points, split 50/50

**50%: execution and understanding**, sub-split for defensibility rather
than one blended number:

- Code and reproduction quality: does the baseline actually run, is the
  extension actually implemented, is it correct.
- Depth of understanding of the current research: can the team explain
  the baseline paper's problem, method, and results accurately, and
  answer questions about it, not just their own added part.

**50%: novelty and value of the extension idea**, also sub-split:

- Motivation and value: is the extension well-motivated by a real,
  specific limitation of the baseline, and is it actually useful, not
  novelty for its own sake.
- Result quality: is the extension evaluated against the baseline with a
  real comparison, and are the results credible, including an honest
  smoke-test result if that is what was run, per the compute-cap
  allowance above.

Every teammate is individually accountable across all four of these in
Q&A, not just the sub-score that maps to the part they personally wrote.

## What this fully removes

- The "Continuous Project" model: one team, one domain, one agent grown
  across five required GitHub issues (one per module).
- The old 8-criterion, 100-point capstone rubric (problem framing,
  understanding/extraction, dialogue management, grounded generation,
  memory, evaluation rigor, ethics/privacy/safety, communication), which
  mapped one-to-one onto the old continuous agent's five built pieces.
  Replaced entirely by the 50/50 structure above.
- Every team building all five capabilities regardless of topic. A team
  now goes deep on one topic; it does not owe the course a working
  extraction pipeline, dialogue manager, grounding pipeline, memory
  layer, and eval harness all at once.
- The old cross-module Q&A mechanic ("ask a teammate about a module they
  did not personally build," using PR history to target questions).
  Replaced by "any teammate, any of paper, extension, or code."

## What stays the same

- The five modules keep teaching their five subjects, in the same order,
  at the same production depth. Nothing about the lecture content's
  *teaching* purpose changes.
- Each module's research-dive material is still valuable on its own
  terms, and now doubles as the way students first encounter candidate
  papers for that topic, before a separate curated menu exists.
- Module 6 remains the defense session; only its internal shape (topics
  instead of one continuous system, new timing, new rubric) changes.

## Still to build (tracked as separate tasks, not decided further here)

1. Fill the research-dive gap in Modules 1 and 2 (currently neither has
   one; both predate that convention).
2. Curate the actual paper-and-repo menu, five topics, papers that
   already have a working repo and fit the compute/cost cap. Done,
   2026-09-17: `research/PROJECT-PAPER-MENU.md`, thirteen papers across
   the five topics, each with a verified repository link and a concrete
   compute/cost note, plus one flagged exception (Dialogue's own taught
   paper has no public repo). Linked from Module 1's kickoff slide.
3. Rewrite Module 1's old "Project kickoff" segment to present the five
   topics, the menu, the selection rules, and the idea-pitch step, so
   teams can start choosing on day one.
4. Rewrite the syllabus's "Continuous Project" and "Assessment" sections,
   and its capstone rubric table, to match this document.
5. Rebuild `dsca-team-template`'s issue templates: the old module-1
   through module-5 templates describe the removed continuous-agent
   deliverables and need replacing with idea-pitch, baseline-reproduction,
   extension, and report/slides templates. Done, 2026-09-17, commit
   `b76e968` in `dsca-team-template`: the old `agent/` five-capability
   stub package and its five issue templates are removed, replaced by
   `baseline/`, `extension/`, `report/REPORT.md`, `slides/README.md`, and
   four matching issue templates. `README.md`, `CONTRIBUTING.md`,
   `.env.example`, `requirements.txt`, and `scripts/verify_setup.py` were
   also rewritten so they no longer assume every team uses the same
   stack (Gemini plus Mem0 or Zep plus ChromaDB), since that now depends
   on which paper each team picked.
6. Rebuild Module 6 itself: segment minutes, the instructor scoring sheet
   for the rubric above, and the defense-day materials.
7. Update `PROGRESS.md` and `index.html`/`README.md` so a new session (or
   a student rereading the site) sees the current model, not the old one.

This document is the thing every one of those seven items gets checked
against, not chat history. If a future decision changes something above,
edit this file in the same change, so it never drifts out of date with
what actually shipped.
