# Module 1 infographic

One self-contained, interactive HTML page, no server needed, open directly
in a browser. Agent-built (not instructor-designed, unlike Module 5's three
infographics), because the instructor asked for this one to be built
in-house, fact-checked against the paper's own text the same discipline as
any other cited number here, and interactive by request: every number and
architecture step is behind a click, kept collapsed by default, to keep the
page uncluttered. Linked from `lectures/dsca-module-01.html`'s speaker
notes (the "The problem: LLMs hallucinate API calls" slide) and from its
own "Before Module 2" reading callout, so students in self-study mode can
reach it too.

- `gorilla.html`, Patil, Zhang, Wang & Gonzalez (2023), arXiv:2305.15334.

## Where the content came from, and what was checked

Every number and claim on this page was checked directly against the
paper's own text, fetched in full from arXiv's HTML rendering
(`arxiv.org/html/2305.15334v1`, no truncation, a short paper), the same
source already verified for `research/module-01/lecture-notes.md`. No
number on this page is invented or approximated beyond the paper's own
rounding; every figure traces to a specific table or sentence:

- The pipeline (dataset curation, self-instruct, retriever-aware training,
  inference, AST verification): Sections 3.1 through 3.3 of the paper.
- The results table (accuracy and hallucination by model, zero-shot):
  Table 1.
- The retriever-aware training gain (+12.37 / +23.46 points): Table 2 and
  its surrounding text.
- The "what this paper does not claim" list: the paper's own Section 6
  (Limitations) and its own admitted, unresolved finding about GPT-3.5
  hallucinating less than GPT-4 (Section 4.1, "Hallucination with LLM").

## The figure

`images/gorilla-pipeline-original-figure.jpg` is the paper's own Figure 3
(its training-and-inference pipeline diagram), fetched directly from
arXiv (`arxiv.org/html/2305.15334v1/llmapi.png`), CC BY 4.0, downscaled to
a small thumbnail (200x125px, roughly 5KB) for reliable embedding. The
page links out to the full-resolution original for anyone who wants to
zoom in. The thumbnail is genuinely the paper's own artwork, not a
redrawn or agent-imagined version of it.

## Why this one is agent-built, unlike Module 5's three

Module 5's three infographics were instructor-designed and handed over as
finished files; an agent's job there was integration and fact-checking
only (`AGENTS.md` §7b). For this module, the instructor asked directly
whether an agent could extract the paper's own figures and build the page
itself, and then asked for it interactive (click to reveal, not
everything shown at once) rather than in any particular existing design
system. This page is the result: real content, fact-checked the same way,
but agent-authored HTML/CSS/JS rather than a delivered template.
