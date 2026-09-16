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
> 0. Check `PROGRESS.md` for this module's row. If `research/module-[N]/lecture-notes.md` does not exist yet, write it first: the module's full teaching content in prose, organised by the syllabus's own segments, at the depth bar `AGENTS.md` §12 sets (a formula where the field has one, a black box opened at least once, cost stated not implied, a named alternative, the metric the field actually uses, a paper read critically where one applies). This is not slide shorthand, a student could learn from it without the deck. It will also be the source for a concept-infographic NotebookLM prompt and for the deck's own prose, so it has to actually be complete, not a bullet outline. Also find one open-access, important paper for the research dive and save it to `research/module-[N]/<first-author>-<year>-<slug>.pdf`. Then hand the instructor two NotebookLM prompts (see `PROGRESS.md`'s per-module section for the exact pattern and wording used on Module 3): one sourced from the paper, for a research infographic and markdown summary; one sourced from `lecture-notes.md`, for a concept infographic. Log both deliveries in `PROGRESS.md` before moving on.
> 1. Read `AGENTS.md` in full. It is the authoring contract and it overrides your own instincts about slide design.
> 2. Open `design-system.html` in a browser. Every component is live there with its markup.
> 3. Read `lectures/_reference.html`. It is the reference implementation, 21 slides, all nine layouts, all twelve components. Match its structure and its writing register.
>
> Then:
> 4. Copy `lectures/_template.html` to `lectures/[slug]-session-[NN].html`.
> 5. Fill in the `<body data-*>` attributes and write the slides, pulling prose from `lecture-notes.md` rather than drafting it fresh against the syllabus row.
> 6. Add a `<a class="lu-lecture-card">` for it in `index.html`.
> 7. Once each NotebookLM prompt's infographic comes back, add it as its own full-page slide (see "Adding an infographic slide" below), not traced into a CSS redraw and not skipped.
> 8. Open it and press `→` through every slide, then `?`, `O`, `/`, `S`, and print preview. Fix anything that throws in the console.
>
> Hard constraints: no `<style>` blocks and no new colours, fonts or sizes; nothing below 20px; every slide needs `data-label`, `data-section`, `data-minutes` and a `<template data-notes>`; every graded component needs a module-prefixed unique `data-qid`; every answer option needs a rationale; diagrams use the CSS primitives first, inline SVG second, a `.lu-figure__ph` placeholder third, never a hand-drawn screenshot; a NotebookLM infographic is its own full-page slide with an honest caption, never traced or forced into a CSS redraw.
>
> Budget **3 to 4 minutes per content slide**, so a 180-minute module in this course is about 24 to 28 slides, plus roughly a minute or two per infographic slide. Aim for 5 to 8 beats per slide, a beat being one thing you can point at and talk to. A divider before every part, a check question after every concept block. End with the wrap slide and the self-check slide, and make the deliverable slide name the GitHub issue it closes.

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
| `research/module-NN/lecture-notes.md` (written before the deck, see `PROGRESS.md`'s build order) | The prose every concept slide's writing draws from, and the source document for the concept-infographic NotebookLM prompt |

---

## Adding an infographic slide

Once a NotebookLM prompt (paper-sourced or `lecture-notes.md`-sourced, see above) comes back with an image, it becomes its own slide, not a redraw and not a background image behind other content. Module 3's two infographic slides are the worked examples, copy their shape:

1. Save the image the instructor sends back into `research/module-NN/` under a name that says its source (`notebooklm-<topic>-reference.png`), then a copy downsized for the web (`sips -Z 1600 …` is enough) into `assets/img/m0N-<topic>-infographic.png`. The `research/` copy is the provenance record, the `assets/img/` copy is what the deck actually serves.
2. Write the slide as a plain sized `<img>` inside a `<figure class="lu-figure">`, not `.lu-figure__frame`, that class is built for `object-fit:cover` photo captures and will silently crop a non-photo image shaped differently from its frame:
   ```html
   <figure class="lu-figure" style="margin-top:var(--lu-s3);align-items:center">
     <img src="../assets/img/m0N-topic-infographic.png" alt="[describe the actual diagram content, this is the only place a non-sighted reader gets it]"
          style="display:block;width:auto;height:auto;max-width:100%;max-height:430px;border-radius:var(--lu-r3)">
     <figcaption>A visual aid for today's reading, not a figure from the paper / not measured from anything in this course (say whichever is true). <a href="…" target="_blank" rel="noopener">Read the paper</a> &middot; <a href="../assets/img/m0N-topic-infographic.png" target="_blank" rel="noopener">open full-size</a>.</figcaption>
   </figure>
   ```
3. Say plainly in the caption and the speaker notes when a number on the image is illustrative rather than measured or paper-verified, so nobody later quotes a NotebookLM-invented figure as this course's own result. When a number on the image **is** paper-verified, that number belongs on the deck's own results slide too (in your own table, checked against the paper directly), the infographic is a visual aid alongside that, not instead of it.
4. Place the slide where all the concepts it depicts have already been taught, not before. Give it 2 minutes in `data-minutes`, and rebalance the module's total back to budget by trimming the most flexible slide (usually the open-ended lab-build slide), never by shaving a concept slide's time.
5. Verify with `scripts/audit-deck.js` like any other slide. A first guess at `max-height` commonly overflows the footer by a small amount (Module 3's two slides did, by 70px and 10px respectively); tighten it and re-run rather than eyeballing it as fine.

---

## Changing the design rather than using it

- **New colour, size, spacing or component** → edit `assets/lu.css` in the right numbered section, add a live demo to `design-system.html` §8, add a cheat-sheet row to `AGENTS.md` §5, bump the `?v=` on the asset links.
- **New interactive behaviour** → `AGENTS.md` §11 has the six steps.
- **Never** solve it with a `<style>` block in a lecture. That is how twelve lectures stop looking like one course.
