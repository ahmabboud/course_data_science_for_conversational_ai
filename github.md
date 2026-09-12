repo: ahmabboud/course_data_science_for_conversational_ai
branch: main
upstream template: ahmabboud/LebUniv_Course_Template @ `39c8880` (v1.1.0)

## Last sync

date: 2026-09-11 (restructure)
commits: `7e1039c` (initial scaffold), `f81e1cf` (Pages status note), this
restructure (not yet committed)
status: Pages is confirmed live (see prior sync entry). This entry is a
course-content restructure, not a template resync.
direction: this repository is DOWNSTREAM of the template. The stylesheet,
runtime, authoring contract and audit script were authored in
`LebUniv_Course_Template`. Defects in `assets/`, `scripts/` or `AGENTS.md`
belong upstream, not here.

## What changed in this restructure, and why

The course changed shape after the initial scaffold, before any lecture was
built. Three decisions drove it:

1. **Schedule.** 9 sessions of 2 hours became 5 modules of 3 hours plus a
   3-hour project defense. Same 18 contact hours, different shape.
2. **Method.** The classical NLP stack (spaCy, scikit-learn, Rasa, hand-authored
   dialogue policies) was dropped entirely. This is now an LLM-only course, so
   the "build it twice, classical then LLM, then compare" pedagogy is gone.
   Every capability is built once, at the depth a production team would build
   it, using LangGraph, MCP, hybrid-search RAG, and Mem0 or Zep for memory.
3. **Project.** There is no longer a late capstone kickoff. Each team of two
   to three chooses its own domain in Module 1 and grows one agent across all
   five modules, one GitHub issue per module, in its own repository. Module 6
   is a live defense of that same system, not a new deliverable.

The syllabus (`Data Science for Conversational AI - Syllabus.docx`, one
directory above this repository) was rebuilt from scratch against this new
shape, anchored to Chip Huyen's *AI Engineering* (2025) and DeepLearning.AI's
*AI Agents in LangGraph* course rather than the previous classical-leaning
anchor. It is the source of truth for every module's objective, segment
minutes, deliverable and reading.

## What changed in this repository

| File | Change |
|---|---|
| `index.html` | Six module cards replacing nine session cards. Module 6 (Defense) is marked "No lecture deck" rather than "Not yet built", since it has no deck to author. |
| `README.md` | Rewritten: module table, the continuous-project description, and a note distinguishing this lecture repository from each team's own project repository. |
| `manifest.webmanifest` | Description updated to "5 modules plus a project defense". |
| `AGENTS.md` | Two localized pointers updated: the file-naming step (`dsca-module-NN.html`, was `dsca-session-NN.html`) and the `<body data-*>` example (`dsca-m01`, `Module 1 of 6`, `data-duration="180"`, was `dsca-s01`, `Session 1 of 9`, `120`). Its pacing guidance in §4 (180-minute session, 24 to 28 slides) did not need to change, since it was already written for 3-hour sessions and this course is 3-hour modules again. |
| `PROMPT.md` | Retargeted the same way, plus: the handoff prompt now says "module" not "session"; the pacing line now correctly says 180 minutes and 24 to 28 slides, correcting the previous entry's 120-minute, 16-to-20-slide figure, which no longer applies; the skeleton step now says ~26 shells, not ~18; a stray, never-applicable line referencing `uploads/LebUniv/` and a nonexistent `syllabus-source.json` was removed from "Where each source file goes"; that section now also says the deliverable field names a GitHub issue, and the slide should say so. |
| `design-system.html` | No change needed this time, its only localized pointer (the worked-example link) already points at `_reference.html`. |

## Naming convention

Lecture files are `lectures/dsca-module-NN.html` for Modules 1 to 5, zero-padded.
Module 6 has no lecture file. Deck ids are `dsca-mNN`. Graded component
`data-qid` values are prefixed with the module, for example `dsca-m03-q1`.

## Deployment

GitHub Pages, source set to **GitHub Actions**. `.github/workflows/pages.yml`
uploads the repository unchanged on every push to `main`. Confirmed live in
the prior sync entry.

## Open items

- This restructure is committed locally but not yet pushed. Run
  `git push origin main` from a machine with GitHub credentials.
- No lecture built yet. Module 1 is the next piece of work.
- Each team's own project repository (for the continuous agent build) does
  not exist yet and is separate from this one. It gets created per team in
  Module 1.
- The `LU` lockup is still the typographic placeholder, not the official crest.
