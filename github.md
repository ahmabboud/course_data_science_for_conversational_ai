repo: ahmabboud/course_data_science_for_conversational_ai
branch: main
upstream template: ahmabboud/LebUniv_Course_Template @ `39c8880` (v1.1.0)

## Last sync

date: 2026-09-11
commits: `7e1039c` (initial scaffold)
status: **committed locally on `main`, not pushed.** Run `git push -u origin main`
from this directory. The push has to happen from a machine with GitHub
credentials.
direction: this repository is DOWNSTREAM of the template. The stylesheet,
runtime, authoring contract and audit script were authored in
`LebUniv_Course_Template`. Defects in `assets/`, `scripts/` or `AGENTS.md`
belong upstream, not here.

## What the initial commit contains

Seeded from `LebUniv_Course_Template` at `39c8880`, then localized for this
course. Everything in `assets/`, `scripts/`, `sw.js` and `.github/` is the
template unchanged.

| File | State |
|---|---|
| `assets/*`, `scripts/audit-deck.js`, `sw.js`, `.github/workflows/pages.yml`, `.gitignore`, `.nojekyll` | Template, byte-identical to `39c8880` |
| `index.html` | Rewritten. Nine session cards from the syllabus, all `aria-disabled` and marked "Not yet built" |
| `README.md` | Rewritten for this course |
| `manifest.webmanifest` | Rewritten. Name, short name, description |
| `AGENTS.md` | Template, with five course pointers retargeted (see below) |
| `PROMPT.md` | Template, with the same retargeting plus the pacing figure corrected to 120-minute sessions |
| `design-system.html` | Template, with the worked-example link retargeted |
| `lectures/_template.html` | Template, unchanged |
| `lectures/_reference.html` | The template's `kr-session-03.html`, renamed. Kept as the worked example the authoring contract tells you to imitate |
| `lectures/dsca-session-NN.html` | None yet |

## Localization applied on top of the template

These are course pointers, not defects. Do not port them upstream.

- `AGENTS.md` and `PROMPT.md` and `design-system.html`: every reference to
  `lectures/kr-session-03.html` now points at `lectures/_reference.html`.
- `AGENTS.md` §3: the `<body data-*>` example now reads `dsca-s01`,
  `Data Science for Conversational AI`, `Session 1 of 9`, `data-duration="120"`.
- `AGENTS.md` §1 step 3: the new-file path is `lectures/dsca-session-NN.html`.
- `PROMPT.md`: pacing corrected from "a 180-minute session is about 24 to 28
  slides" to "a 120-minute session in this course is about 16 to 20 slides",
  and the skeleton step from ~20 shells to ~18. This course runs 2-hour
  sessions, not the 3-hour sessions the template was written against. Copying
  the Knowledge Representation slide counts will overrun every session.
- `PROMPT.md`: the syllabus-source table now points at
  `Data Science for Conversational AI - Syllabus.docx`, one directory above the
  repository, rather than the Knowledge Representation JSON.

## Naming convention

Lecture files are `lectures/dsca-session-NN.html`, zero-padded. Deck ids are
`dsca-sNN`. Graded component `data-qid` values are prefixed with the session,
for example `dsca-s03-q1`.

## Deployment

GitHub Pages, source set to **GitHub Actions**. `.github/workflows/pages.yml`
uploads the repository unchanged on every push to `main`. There is no build
step. Pages must be enabled once in the repository settings before the first
deployment will succeed.

## Open items

- Pages source not yet configured in repository settings.
- No lecture built yet. Session 1 is the next piece of work.
- The `LU` lockup is still the typographic placeholder, not the official crest.
