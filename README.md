# Data Science for Conversational AI, Lebanese University, MSc

Interactive HTML lectures for the Data Science for Conversational AI course. 18 contact hours, 5 modules of 3 hours plus a 3-hour project defense. Static pages, no build step, deployed to GitHub Pages as-is.

**Students:** open the site and pick a module. Nothing to install. Your answers and your place in a lecture are stored in your own browser and never transmitted.

## The course in one paragraph

This is an LLM-only course: there is no classical NLP stack and no build-it-twice comparison, every capability is built once, at production depth. There is also no separate capstone. From Module 1, each team of two to three picks its own domain and grows one conversational agent across the whole course, one GitHub issue per module. Module 1 gets the agent understanding requests with structured extraction. Module 2 gives it a real multi-turn policy on LangGraph, with one routing or escalation pattern. Module 3 grounds its answers in a retrieved source. Module 4 gives it memory across separate sessions. Module 5 builds the evaluation harness that probes it for correctness, bias and PII leakage. Module 6 is a live defense of the same system, evidence and all, not a new deliverable.

## Modules

| # | Title | Status |
|---|---|---|
| 1 | Foundations and Modern Understanding | To build |
| 2 | Agentic Dialogue Management | To build |
| 3 | Grounded Generation | To build |
| 4 | Memory | To build |
| 5 | Evaluation and Responsible Deployment | To build |
| 6 | Project Defense | No lecture deck, live session only |

Module length is 180 minutes. At the deck pacing of 3 to 4 minutes per content slide, a 3-hour module lands around 24 to 28 slides including dividers and the wrap, the same pacing the Knowledge Representation reference deck uses. Module 6 has no lecture deck to build: it is a live demo and defense session.

## Repository

- **`index.html`**, the course index students land on.
- **`lectures/dsca-module-NN.html`**, one self-contained lecture per file, for Modules 1 to 5.
- **`design-system.html`**, the design system and a live gallery of all twelve interactive components. Start here before authoring.
- **`lectures/_template.html`**, copy this to start a new module.
- **`lectures/_reference.html`**, a fully built deck from the Knowledge Representation course, kept as a worked example of the structure. It is not part of this course and is not linked from the index.
- **`AGENTS.md`**, the authoring contract. Read it before writing a lecture, whether you are a person or an agent.
- **`PROMPT.md`**, the paste-ready brief for handing a new module to an agent.

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
- Each team needs its own GitHub repository for the continuous project, seeded in Module 1. That repository is separate from this one: this repository holds the lecture decks, team repositories hold the agents students build.

## Accessibility

Built to WCAG 2.2 AA, with the contract and one stated exception documented in `design-system.html` §10.

## Licence

Course content belongs to its authors. The template, stylesheet and runtime are yours to reuse and adapt.
