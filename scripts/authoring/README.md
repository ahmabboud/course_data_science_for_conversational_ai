# Authoring helpers for decks (optional)

`lib.py` is a small Python helper for writing slides in the clarity-first style
(AGENTS.md section 2c) without hand-typing JSON for diagrams. It is **a one-off
authoring aid, not a build system**: the lecture HTML files are the hand-edited
source. Write a throwaway builder script that uses `lib.py`, generate the deck
once, then keep editing the HTML directly. Do not re-run a builder over a deck
that has been edited by hand, the edits would be lost.

What it gives you (see the docstrings, and `example_build_project_guide.py`, a
complete 26-slide deck built with it):

- `N(id, label, kind, x, y, w, h)` a diagram node, `E(id, from, to, label)` an
  arrow, `S(show, run, set)` one animation step, `spec(...)` and `static_spec(...)`
  the diagram specification (format: header comment of `assets/lu-flow.js`).
- `flow_walk(label, spec, captions)` an animated diagram stepped with the walk bar,
  `flow_static(spec)` a picture that does not change, `code_walk(...)` and
  `html_walk(...)` walkthroughs whose steps are code or any HTML.
- `slide(label, section, minutes, eyebrow, title, body, notes)` one slide, `divider(...)`
  a dark part divider, `callout`, `table`, `code`, `figure` (a cropped paper figure
  with caption and "Open full size" link).

Rules that still apply (they cost real time before): node text is about 13 units per
character, keep every node inside the 1448-unit canvas, keep a diagram at about 290
units high when a definition box sits below it, leave a gap between two nodes of at
least the arrow label's width, and run `scripts/audit-headless.py` (or
`scripts/audit-deck.js` in the console) after building. `slide()` adds a tighter
gap automatically when a slide has both a walkthrough and a callout.
