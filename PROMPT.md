# Paste-ready brief for building a new session

Two ways to use this repository. Pick one.

---

## A · Hand it to an agent (recommended)

Give the agent access to the repository, then paste this, filling the four bracketed fields:

> Build module **[N]** of **[COURSE NAME]** as an interactive HTML lecture in this repository.
>
> **Source material:** [path to the syllabus file, or paste the module's objective, segments, minutes, deliverable and reading]
>
> Before you write anything:
> 1. Read `AGENTS.md` in full. It is the authoring contract and it overrides your own instincts about slide design.
> 2. Open `design-system.html` in a browser. Every component is live there with its markup.
> 3. Read `lectures/_reference.html`. It is the reference implementation, 21 slides, all nine layouts, all twelve components. Match its structure and its writing register.
>
> Then:
> 4. Copy `lectures/_template.html` to `lectures/[slug]-session-[NN].html`.
> 5. Fill in the `<body data-*>` attributes and write the slides.
> 6. Add a `<a class="lu-lecture-card">` for it in `index.html`.
> 7. Open it and press `→` through every slide, then `?`, `O`, `/`, `S`, and print preview. Fix anything that throws in the console.
>
> Hard constraints: no `<style>` blocks and no new colours, fonts or sizes; nothing below 20px; every slide needs `data-label`, `data-section`, `data-minutes` and a `<template data-notes>`; every graded component needs a module-prefixed unique `data-qid`; every answer option needs a rationale; diagrams use the CSS primitives first, inline SVG second, a `.lu-figure__ph` placeholder third, never a hand-drawn screenshot.
>
> Budget **3 to 4 minutes per content slide**, so a 180-minute module in this course is about 24 to 28 slides. Aim for 5 to 8 beats per slide, a beat being one thing you can point at and talk to. A divider before every part, a check question after every concept block. End with the wrap slide and the self-check slide, and make the deliverable slide name the GitHub issue it closes.

That is the whole handoff. The agent needs nothing else from you.

---

## B · Build it yourself

```
cp lectures/_template.html lectures/dsca-module-01.html
```

Then, in order:

1. **`<body>` attributes**, `data-deck-id` (unique, e.g. `dsca-m01`), `data-course`, `data-session`, `data-duration`, `data-app-root="../"`, `data-unit`.
2. **Title slide**, module tag, eyebrow, title, one-sentence objective, the time split.
3. **Slide skeleton first, prose second.** Lay out ~26 `<section class="slide">` shells with only `data-label`, `data-section` and `data-minutes` filled in, and check the minutes sum to your contact time (180). Fixing pacing later means rewriting slides.
4. **Write each slide**, picking the layout from `AGENTS.md` §4.
5. **Notes as you go**, not at the end. What to say, what to cut if behind, the question the room will ask.
6. **Add the card to `index.html`.**
7. **Walk it** with `→`, then `S` for study mode, then print preview.

---

## Where each source file goes

This course's syllabus is `Data Science for Conversational AI - Syllabus.docx`,
one directory above the repository, with `CourseObjectives.txt` beside it. The
objectives file gives the arc; the docx carries the module breakdown, and each
module there already has an objective, a segment table with minutes, a
deliverable and a reading. Extract that module's row before you write a slide,
and reconcile your `data-minutes` against its segment budget (180 total).

The syllabus fields map onto slides directly:

| Syllabus field | Becomes |
|---|---|
| Module `objective` | The title slide's lead sentence |
| Module `segments` (name, minutes, text) | The section dividers and the `data-minutes` budget |
| Segment text, sentence by sentence | Concept slides. One idea per slide; the prose becomes speaker notes |
| Module `deliverable` | The deliverable callout on the lab-brief slide. It names a GitHub issue (e.g. "Issue 3 merged: ..."), say so on the slide, not just the underlying work |
| Module `reading` | The "Before next module" callout on the wrap slide |
| `module` field in `Course Structure` | The tag on the title slide and `data-section` values |
| Misconceptions named in the text | Check questions, not bullets. Name the specific wrong belief the question is testing for |
| `rubric` rows touching this module (in the syllabus's continuous-project rubric) | What the lab-brief slide says is graded |

---

## Changing the design rather than using it

- **New colour, size, spacing or component** → edit `assets/lu.css` in the right numbered section, add a live demo to `design-system.html` §8, add a cheat-sheet row to `AGENTS.md` §5, bump the `?v=` on the asset links.
- **New interactive behaviour** → `AGENTS.md` §11 has the six steps.
- **Never** solve it with a `<style>` block in a lecture. That is how twelve lectures stop looking like one course.
