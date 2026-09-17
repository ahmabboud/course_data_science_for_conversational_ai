# Module 2 infographic

One self-contained, interactive HTML page, no server needed, open directly
in a browser. Agent-built (not instructor-designed, unlike Module 5's
three infographics), for the same reason as Module 1's: the instructor
asked for it built in-house, fact-checked, and interactive by request,
every number and architecture step behind a click, kept collapsed by
default, to keep the page uncluttered. Linked from
`lectures/dsca-module-02.html`'s speaker notes (the "The problem: triage
is slow, manual, and easy to misroute" slide) and from its own "Before
Module 3" reading list, so students in self-study mode can reach it too.

- `helping-customers-in-distress.html`, Atreya et al. (2026),
  arXiv:2605.16268.

## Where the content came from, and what was checked

Every number and claim on this page was checked directly against the
paper's own text, fetched in full from arXiv's HTML rendering
(`arxiv.org/html/2605.16268v1`, no truncation), the same source already
verified for `research/module-02/lecture-notes.md`. No number on this page
is invented or approximated beyond the paper's own rounding; every figure
traces to a specific table or sentence:

- The architecture (Triage Agent, Handoff agent, Guardrail agents): the
  paper's system description sections and its own Figure 1.
- The results (best synthetic gain, SME-tested gain, handoff
  precision/recall, guardrail accuracy): Table 1 and its surrounding
  text, including confidence intervals reported there.
- The gap between the synthetic-testing figure (+30.6%) and the
  SME-tested figure (+16.0%): the paper's own comparison of its digital
  twin results against its human expert review, called out on this page
  as a limit rather than smoothed over.
- The "what this paper does not claim" list: the paper's own stated
  limitations around evaluation scope and generalization.

## The figure

`images/triage-workflow-original-figure.jpg` is the paper's own Figure 1
(its triage-and-handoff architecture diagram), fetched directly from
arXiv (`arxiv.org/html/2605.16268v1/figures/workflow_triage4.png`), CC BY
4.0, downscaled to a small thumbnail (220x141px, roughly 4KB) for reliable
embedding. The page links out to the full-resolution original for anyone
who wants to zoom in. The thumbnail is genuinely the paper's own artwork,
not a redrawn or agent-imagined version of it.

## Why this one is agent-built, unlike Module 5's three

Module 5's three infographics were instructor-designed and handed over as
finished files; an agent's job there was integration and fact-checking
only (`AGENTS.md` §7b). For this module, as for Module 1, the instructor
asked directly whether an agent could extract the paper's own figures and
build the page itself, then asked for it interactive rather than in any
particular existing design system. This page is the result: real content,
fact-checked the same way, but agent-authored HTML/CSS/JS rather than a
delivered template.
