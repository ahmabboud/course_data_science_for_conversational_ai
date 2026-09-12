# Data Science for Conversational AI, Lebanese University, MSc

Interactive HTML lectures for the Data Science for Conversational AI course. 18 contact hours, 9 sessions of 2 hours. Static pages, no build step, deployed to GitHub Pages as-is.

**Students:** open the site and pick a session. Nothing to install. Your answers and your place in a lecture are stored in your own browser and never transmitted.

## The course in one paragraph

One conversational agent, built end to end. Every capability is built twice: first with classical NLP components so the mechanics stay visible, then with LLM-based components, and the two are compared on quality, latency and cost. Design an intent and slot schema and annotate against it, train and calibrate intent classifiers, extract and normalize entities under a schema, drive multi-turn behaviour from explicit dialogue state, ground responses in a retrieved source with citation and a working refusal path, then measure the result with a regression harness that also probes for bias and PII leakage. Sessions 8 and 9 are the capstone, where teams integrate all of it and defend it with evidence.

## Sessions

| # | Module | Title | Status |
|---|---|---|---|
| 1 | 1 | Foundations of Conversational AI and System Architecture | To build |
| 2 | 1 | Conversational Data, Corpora, and Annotation | To build · Milestone 1 |
| 3 | 2 | Intent Recognition | To build |
| 4 | 2 | Entity Extraction and Slot Filling | To build |
| 5 | 3 | Dialogue Management and State Tracking | To build |
| 6 | 3 | Response Generation, Knowledge Grounding, and Capstone Kickoff | To build |
| 7 | 4 | Evaluation, Bias, Privacy, and Deployment | To build · Milestone 2 |
| 8 | 5 | Capstone Build Lab | To build |
| 9 | 5 | Capstone Evaluation, Demonstration, and Course Close | To build |

Session length is 120 minutes. At the deck pacing of 3 to 4 minutes per content slide, a 2-hour session lands around 16 to 20 slides including dividers and the wrap, which is smaller than the 3-hour Knowledge Representation decks. Do not copy their slide counts.

## Repository

- **`index.html`**, the course index students land on.
- **`lectures/dsca-session-NN.html`**, one self-contained lecture per file.
- **`design-system.html`**, the design system and a live gallery of all twelve interactive components. Start here before authoring.
- **`lectures/_template.html`**, copy this to start a new session.
- **`lectures/_reference.html`**, a fully built deck from the Knowledge Representation course, kept as a worked example of the structure. It is not part of this course and is not linked from the index.
- **`AGENTS.md`**, the authoring contract. Read it before writing a lecture, whether you are a person or an agent.
- **`PROMPT.md`**, the paste-ready brief for handing a new session to an agent.

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
- The course syllabus lives one directory up, in `Data Science for Conversational AI - Syllabus.docx`. Session objectives, segment minutes, deliverables and readings all come from it. A deck whose section minutes do not sum to the syllabus budget will overrun.

## Accessibility

Built to WCAG 2.2 AA, with the contract and one stated exception documented in `design-system.html` §10.

## Licence

Course content belongs to its authors. The template, stylesheet and runtime are yours to reuse and adapt.
