# Module 5 infographics

Three self-contained, interactive HTML pages, no server needed, open any
of them directly in a browser. Instructor-designed (Clearpaper template),
not agent-authored, then fact-checked against each paper before being
linked into the course, the same discipline as any other cited number
here. Linked from `lectures/dsca-module-05.html`'s speaker notes (the
tau-bench, tau2-bench, and trajectory-judge slides) and from its own
"Before Module 6" reading list, so students in self-study mode can reach
them too.

- `tau-bench.html`, Yao, Shinn, Razavi & Narasimhan (2024), arXiv:2406.12045.
- `tau2-bench.html`, Barres, Dong, Ray, Si & Narasimhan (2025), arXiv:2506.07982.
- `trajectory-judge.html`, Mohammadi (2026), arXiv:2609.00038.

## Where these came from, and what was checked

Each page's claims were checked against the paper's own text, fetched
directly from arXiv (`arxiv.org/abs/<id>` and, where the fetch succeeded,
`arxiv.org/html/<id>v1`). No fabricated or incorrect number was found in
any of the three; nothing needed a caption fix. What follows is exactly
what was and was not independently confirmed, so a future session does
not have to re-derive this.

### `trajectory-judge.html`: fully verified

Every claim on this page was checked directly against the paper's full
text (fetched in full, all sections reachable) and confirmed accurate:

- Outcome-only judge: 84% loud-fault recall, 45% silent-fault recall,
  33% false-alarm rate on clean trajectories. Matches the paper's Table 3
  and its own abstract.
- Step-rubric judge: 77% silent-fault recall, zero false alarms (0 of 100
  clean trajectories, a genuine observed 0, not a rounded-down small
  number; the paper's own 95% upper confidence bound on that zero is
  3.6%), costs 3x the outcome-only judge.
- Step-rubric judge's 98% loud-fault recall (the infographic's group-
  compare chart): confirmed, the paper's step(14B) judge scores 0.984 on
  loud-fault recall, which rounds to 98%. Note this is the 14B-model step
  judge specifically; the paper's separate 8B-model step judge behaves as
  a degenerate always-flag baseline and is not what this infographic's
  98% figure refers to.
- "An invented promise slips past the step judge 82% of the time":
  confirmed verbatim in the paper's abstract and body.
- The two model sizes behind the step-rubric judge (14B and 8B): confirmed
  as `qwen2.5:14b` and `llama3.1:8b` respectively, Table 2.
- Six fault types: confirmed, `|Φ|=6` in the paper's own notation:
  skipped_precondition, hallucinated_argument, ignored_observation,
  premature_stop, wrong_tool, unsupported_claim (the "invented promise"
  case above is this last one).
- 400 trajectories, 5 judges compared: confirmed.

### `tau-bench.html`: headline figures verified, per-model bars and failure breakdown not independently confirmed in this pass

Confirmed directly against the paper's abstract and introduction:

- "Best agent solved under half the tasks" and "pass^8 < 25% in retail":
  the paper's own abstract states this almost verbatim (state-of-the-art
  agents "succeed on <50% of the tasks," pass^8 "<25% in retail").
- gpt-4o scores ~61% pass^1 on tau-retail and ~35% on tau-airline: both
  confirmed in the paper's introduction ("∼61% on tau-retail," "∼35% on
  tau-airline").
- 165 total tasks: confirmed as the sum of the paper's own per-domain
  counts (115 retail + 50 airline = 165), Table 1.

**Not independently confirmed in this pass** (the fetched copy of the
paper was cut off before the results tables and appendices that would
carry these; a secondary, non-primary source found by web search was
consistent with some of these but is not treated as verification):

- claude-3-opus at 44% and gpt-3.5-turbo at 20% (the per-model comparison
  bars). Only gpt-4o's headline numbers were reachable in the text
  actually fetched.
- The failure-cause breakdown (wrong argument 33%, wrong decision 25%,
  wrong info 22%, partial job 19%, out of 36 gpt-4o failures). A web
  search surfaced a "wrong decision: 25%" figure consistent with this
  chart, but could not confirm the other three categories from a source
  that clearly matches this specific breakdown, so this is noted as
  unconfirmed rather than accurate or wrong.
- "gpt-4o lost 22 points on airline without the policy/rulebook": not
  found in the text actually fetched; the paper likely has this ablation
  in a section this pass did not reach.

### `tau2-bench.html`: headline figures verified, the step-count chart not independently confirmed in this pass

Confirmed directly against the paper's own text:

- 114 tasks generated from 2,285 combinations (telecom domain): confirmed,
  Table 1.
- gpt-4.1 scores 34% pass^1 in default (dual-control) mode on telecom:
  confirmed in the introduction.
- "Fake users still err in 16% of chats": confirmed, the paper states a
  16% overall user-simulator error rate for telecom (with a separate,
  lower 6% critical-error rate; the infographic's caveat says "err in
  16% of chats," which matches the overall rate, not the critical-error
  rate, so this line is accurate as worded).
- 52% pass^1 acting alone (no-user/oracle mode) and the resulting -18
  point drop to 34% in default mode: the paper's introduction confirms a
  "substantial performance decrease (around 20% pass^1)" moving from
  no-user to dual-control, consistent with an 18-point drop for this
  specific model, but the fetched text was cut off before the results
  table that would state gpt-4.1's exact no-user-mode score, so the 52%
  figure itself is not independently pinned down from the primary text in
  this pass. A secondary source (not the paper itself) is arithmetically
  consistent with 52% and -18 points.

**Not independently confirmed in this pass:** the step-count "cliff"
chart (success rate by number of steps needed to solve the task: roughly
92/70/52/34/18/4% for 2 through 7+ steps). The fetched text was cut off
before the section that would report this breakdown.

## Why some of this could not be checked further here

This sandbox's page-fetch tool returned the arXiv HTML rendering of each
paper, but truncated tau-bench's copy before its results tables
(Section 5) and appendices, and truncated tau2-bench's copy before its
results section (Section 4) entirely. trajectory-judge's much shorter
paper fetched in full. Re-running the unconfirmed items above needs
either the actual PDF (this sandbox cannot reach arXiv's PDF endpoint,
the same standing limitation already logged in `PROGRESS.md`'s Module 5
paper track) or a fetch of the remainder of the two truncated HTML pages
from an environment that can pull more than the first ~200-1000 lines.
Nothing above was found to be wrong: the unconfirmed items are simply
unconfirmed, not contradicted.
