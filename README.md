# Data Science for Conversational AI, Lebanese University, MSc

Interactive HTML lectures for the Data Science for Conversational AI course. 18 contact hours, 5 modules of 3 hours plus a project defense, extendable by up to 1 hour depending on team count. Static pages, no build step, deployed to GitHub Pages as-is.

**Students:** open the site and pick a module. Nothing to install. Your answers and your place in a lecture are stored in your own browser and never transmitted.

## The course in one paragraph

This is an LLM-only course: there is no classical NLP stack and no build-it-twice comparison, every capability is built once, at production depth. There is also no separate capstone. Each team of up to three picks one of five topics (extraction, dialogue, grounding, memory, or evaluation, one per module) and one paper, from a curated menu or self-proposed, reproduces that paper's baseline, and builds a novel, useful extension of it. Module 1 teaches structured extraction and starts team formation and topic selection. Module 2 teaches agentic dialogue management on LangGraph. Module 3 teaches grounded generation. Module 4 teaches memory. Module 5 teaches multi-turn evaluation, bias, and PII probing. Module 6 is the live defense: each team presents its baseline and extension for 12 minutes and takes 12 minutes of questions on any part, the paper, the extension, or the code. See `PROJECT-REDESIGN.md` for the full project design and `research/PROJECT-PAPER-MENU.md` for the curated paper menu.

## Modules

| # | Title | Status |
|---|---|---|
| 1 | Foundations and Modern Understanding | Built |
| 2 | Agentic Dialogue Management | Built |
| 3 | Grounded Generation | Built |
| 4 | Memory | Built |
| 5 | Evaluation and Responsible Deployment | Built |
| 6 | Project Defense | No lecture deck, live session only, see `module-06-defense/` |

Module length is 180 minutes. At the deck pacing of 3 to 4 minutes per content slide, a 3-hour module lands around 24 to 33 slides including dividers and the wrap, the same pacing the Knowledge Representation reference deck uses. Module 6 has no lecture deck: it is a live demo and defense session, run from `module-06-defense/DEFENSE-DAY.md` and its scoring sheet, not a slide deck.

## Repository

- **`index.html`**, the course index students land on.
- **`lectures/dsca-module-NN.html`**, one self-contained lecture per file, for Modules 1 to 5.
- **`design-system.html`**, the design system and a live gallery of all thirteen interactive components. Start here before authoring.
- **`lectures/_template.html`**, copy this to start a new module.
- **`lectures/_reference.html`**, a fully built deck from the Knowledge Representation course, kept as a worked example of the structure. It is not part of this course and is not linked from the index.
- **`AGENTS.md`**, the authoring contract. Read it before writing a lecture, whether you are a person or an agent.
- **`PROMPT.md`**, the paste-ready brief for handing a new module to an agent.
- **`PROGRESS.md`**, read this first. Tracks, per module, the research-paper track, the graphics track, and the code test/readiness track, so a new session knows what is done and what is next without re-deriving it.
- **`research/module-NN/`**, that module's `lecture-notes.md` (the full content, written before the deck, and the source for its concept-infographic NotebookLM prompt), the paper(s) downloaded for the research dive, and any NotebookLM output worth keeping for provenance.
- **`research/PROJECT-PAPER-MENU.md`**, the curated paper-and-repo menu for the team project: two to four candidate papers per topic, each with a verified, working repository and a compute/cost note.
- **`demos/`**, instructor-only demo material used live during specific lectures, a notebook for one module, a `langgraph dev` / Studio demo for another. See `demos/README.md` for the setup steps and which demo belongs to which lecture, both directions of that link matter.
- **`assets/infographics/module-NN/`**, standalone interactive or reference infographics for a module's research dive, linked from the deck's speaker notes and reading slide, never embedded inline. See each folder's own `README.md` for fact-check provenance.
- **`module-06-defense/`**, Module 6's own materials since it has no lecture deck: `DEFENSE-DAY.md` (the instructor's run-of-show) and `scoring-sheet.xlsx` (the fillable schedule and rubric).
- **`PROJECT-REDESIGN.md`**, the locked source of truth for the team project's design: the five topics, paper selection rules, the idea-pitch and related-work guardrails, deliverables, defense-day format, and the 100-point rubric.

Built from the [`LebUniv_Course_Template`](https://github.com/ahmabboud/LebUniv_Course_Template) design system. Fixes to the stylesheet or runtime belong upstream in the template, not here.

## What a lecture gives you

Presenter view on a second screen with speaker notes, elapsed time and pacing against the plan · deep-linkable slides (`#/12`) · contents panel and full-text search · a study mode that expands every popover, held-back answer and build step · one-page-per-slide printing with the instructor notes attached · offline support once installed · answers and position saved on the student's own device.

## Run it locally

Open any HTML file directly in a browser. Everything works from `file://` except the offline service worker, which needs `http`:

```
python3 -m http.server 8000
```

## Deploy

Enable GitHub Pages with **GitHub Actions** as the source, then push to `main`. `.github/workflows/pages.yml` uploads the repository unchanged. There is no build step.

## Before teaching from it

- Replace the `LU` placeholder in the lockup with the official crest at `assets/lu-crest.svg`. The mark here is a typographic stand-in, not the university's emblem.
- Replace every `.lu-figure__ph` placeholder with a real capture. Each one states the path and what must be visible in the shot.
- The course syllabus lives one directory up, in `Data Science for Conversational AI - Syllabus.docx`. Module objectives, segment minutes, deliverables and readings all come from it, and each deliverable names the GitHub issue it corresponds to. A deck whose section minutes do not sum to the syllabus budget will overrun.
- Each team needs its own GitHub repository created from `dsca-team-template`, seeded once they pick a topic and paper in Module 1. That repository is separate from this one: this repository holds the lecture decks, team repositories hold each team's baseline reproduction and novel extension.
- `demos/module-01/hook_demo.ipynb` is the Module 1 hook, instructor only; `demos/module-02/` is a `langgraph dev` / Studio demo for Module 2. See `demos/README.md` for one-time shared setup, then each module's own `demos/module-NN/README.md` for exact run steps.

## Accessibility

Built to WCAG 2.2 AA, with the contract and one stated exception documented in `design-system.html` §10.

## Licence

Course content belongs to its authors. The template, stylesheet and runtime are yours to reuse and adapt.
