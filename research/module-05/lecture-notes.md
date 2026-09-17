# Module 5: Evaluation and Responsible Deployment, lecture notes

Written before the deck, matching Module 4's own build order. This is the
source the slide deck's prose gets pulled from, the source for any
concept-infographic prompt, and it is posted for students as extended
reading in its own right. Organised by this module's syllabus segments
(`Data Science for Conversational AI - Syllabus.docx`, Session 5, rebalanced
this pass): Lecture (50 min), Research dive (40 min), Hands-on lab (60 min),
Discussion and wrap (30 min).

**Objective** (from the syllabus). Decide, with evidence, whether the agent
built over the last four modules is actually good and safe to put in front
of users.

Every fact below was read directly from each paper's own arXiv abstract
page (and, for tau-bench, its full text) on 2026-09-16, not reconstructed
from memory or from a secondary summary. These four papers could not be
downloaded as PDFs into this repository the way Module 4's three were
(no outbound fetch to arxiv.org's PDF endpoint from this environment); the
arXiv links below are the citable source until a PDF copy is added.

---

## 1. Lecture, part one: component metrics lie about the whole system (~15 min)

A conversational agent is a pipeline: extraction, retrieval, memory, tool
calls, generation. It is tempting to grade each stage on its own held-out
set and call the system validated once every stage clears its bar. This is
exactly the mistake this module exists to correct.

**The compounding-error problem, stated plainly.** If five independent
pipeline stages each succeed 95% of the time, a conversation that needs all
five to succeed in the same turn succeeds only `0.95^5 ≈ 77%` of the time,
and a real multi-turn conversation needing all five stages to keep
succeeding across, say, six turns in a row succeeds `0.95^30 ≈ 21%` of the
time. No single component metric on this system would ever show a number
below 95%; the system's actual, end-to-end reliability is nowhere near
that. This is the formal reason "every component passed" and "the agent
works" are different claims, worth deriving on the board, not just
asserting.

**The metric this module's research-dive papers introduce to measure the
real thing:** tau-bench's **pass^k** (Yao, Shinn, Razavi & Narasimhan, 2024,
*"tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World
Domains,"* arXiv:2406.12045). Run the same task k times, independently, and
report the fraction of runs where the agent succeeds *every single time*,
not just once. A system can look excellent at pass^1 (does it succeed
once?) and be unusable at pass^8 (does it succeed reliably, every time a
real user tries the equivalent task?). tau-bench's own headline result:
even gpt-4o-class function-calling agents succeed on under 50% of tasks at
pass^1, and fall under 25% at pass^8 in its retail domain. That gap, not
either number alone, is the finding worth putting in front of students.

Two things worth naming about how tau-bench actually scores a run, since
it is not LLM-as-judge: it compares the **database state at the end of the
conversation against an annotated goal state**, a deterministic, faithful
check, precisely because a clean ground-truth state exists in its retail
and airline domains. Section 2 below, and this module's research dive,
is about what happens when that clean ground truth is not available and a
team reaches for an LLM judge instead.

### 1.1 Trajectory-level metrics, and why simulated users are not enough

tau2-bench (Barres, Dong, Ray, Si & Narasimhan, 2025, *"tau2-Bench:
Evaluating Conversational Agents in a Dual-Control Environment,"*
arXiv:2506.07982) pushes the same idea one step further: most benchmarks,
tau-bench included, let only the **agent** call tools, while the user
stays a passive source of information. tau2-bench's telecom domain is
**dual-control**: both the agent and the simulated user can call tools to
change a shared, dynamic environment (modelled formally as a
Dec-POMDP), the way a real technical-support call actually works, the
customer restarts their own router while the agent walks them through it.
The paper's headline finding: agent performance drops **significantly**
the moment the user can act too, and the paper's own ablations separate
*reasoning* failures (the agent chose the wrong thing to do) from
*communication/coordination* failures (the agent could not successfully
guide the user to do their half correctly). That split matters
operationally: the fix for one is better prompting or a better model, the
fix for the other is a clearer, more constrained way of instructing the
user, a genuinely different kind of bug.

### 1.2 Bias probing in generated responses (~10 min)

Persona-conditioned bias in plain chatbot *text* is well documented; this
module's lecture makes the newer, sharper claim: persona conditioning
changes agent *task performance*, not just tone. Cao, Sun & Yue (2026,
*"From Biased Chatbots to Biased Agents: Examining Role Assignment Effects
on LLM Agent Robustness,"* accepted to the AAAI 2026 TrustAgent Workshop,
arXiv:2602.12285) ran the same agentic tasks (strategic reasoning,
planning, technical operations) with only a demographic persona cue
changed, task-irrelevant to what the agent was actually asked to do, and
found performance variations of **up to 26.2%** across widely deployed
models and task types. The mechanism worth showing directly: hold the
task fixed, swap only the identity cue attached to it, and measure the
delta. A system that only ever tests one persona has simply never
measured whether this failure mode exists in its own agent.

### 1.3 PII detection and redaction, retention, and regional regulation (~15 min)

**The mechanism**, matching how Microsoft's Presidio (the field's most
widely deployed open building block for this) is actually built: no single
technique catches everything, so a real pipeline layers regex and deny-list
matching (catalog formats: emails, phone numbers, national ID patterns),
checksum validation (a credit-card-shaped string that fails Luhn is not a
real card number), named-entity recognition for the free-text cases a
pattern cannot catch (a name or address mentioned in prose), and
contextual signals (the word "SSN:" right before a nine-digit string is a
stronger signal than the digits alone). Detection feeds one of several
operators: redact (delete), mask (`***-**-1234`), hash (one-way,
still linkable across records), replace (a synthetic stand-in), or
encrypt (reversible, for an authorised later lookup).

**The cost this mechanism does not advertise.** Redaction is not free:
replacing "user's email is X" with "user's email is [REDACTED]" also
destroys the agent's own ability to answer "what's the email you have on
file for me," a legitimate request, not an attack. This is precisely why
Module 4's memory work and this module's PII work are the same problem
looked at from two directions, what a memory system chooses to store is
exactly what a PII pipeline downstream has to account for.

**Regulation, stated precisely, not vaguely.** As of **August 2, 2026**,
the EU AI Act's Article 50 transparency obligations are binding law: any
conversational AI system deployed to a user in the EU must disclose, in
plain terms, that the user is talking to an AI, not a person. Penalties run
up to EUR 15 million or 3% of global turnover. Separately, and worth
stating so as not to overclaim, the Act's high-risk-system obligations
(Annex III) were deferred by the EU's November 2025 Digital Omnibus, to
December 2, 2027 for standalone high-risk systems. A team's own agent is
very unlikely to be classified high-risk, but if it is deployed anywhere
an EU user could reach it, Article 50's disclosure duty is already live
law today, not a future compliance date.

### 1.4 Deployment concerns: latency budgets, cost per conversation, drift (~10 min)

Three production concerns that never show up in an offline eval at all:

- **Latency budgets.** A p50 latency looks fine while a p95 or p99 tail
  quietly ruins the experience for one user in twenty; a real budget is
  stated per percentile, not as one average number, and it has to account
  for every hop in the pipeline (retrieval, memory search, the generation
  call itself, a possible rerank pass), not just the model call.
- **Cost per conversation**, not cost per call. A single conversation that
  triggers a memory search, a retrieval pass, a rerank, and a multi-turn
  judge at the end has several billed calls behind one user-visible
  reply; the number worth tracking is the sum across a whole conversation,
  the unit a user and a budget actually experience.
- **Drift**, the one deployment risk that is invisible in any offline
  eval: a model provider updates the underlying model behind a pinned
  version string, or a prompt that worked well against last month's model
  behaves differently against this month's, and nothing in the code
  changed. This is the exact, concrete reason this course's own demos pin
  an explicit model version string in every module rather than "latest,"
  worth pointing at directly: this module's deployment-concerns slide is
  not abstract, it is the same discipline the students have been doing
  since Module 1, named and explained for the first time.

---

## 2. Research dive: the documented blind spot in LLM-as-judge grading (~40 min)

**Papers.** tau-bench (arXiv:2406.12045) and tau2-bench (arXiv:2506.07982),
both introduced above, get their full depth here: the pass^k formalism
worked through on the board, and tau2-bench's dual-control performance
drop with its reasoning-vs-coordination split. The third paper is the one
that answers the syllabus's own framing question directly.

**"trajectory-judge: What Outcome-Only LLM Judges Miss on Agent
Trajectories"** (Mohammadi, 2026, arXiv:2609.00038, 16 pages, under review
at a NeurIPS 2026 workshop). Say the evidentiary weight out loud before the
numbers: this is a single-author preprint, not yet peer-reviewed, exactly
the kind of source this course's own critical-reading standard exists for.
It earns its place anyway because it measures precisely the thing the
syllabus asks about, with ground truth known by construction, not
estimated.

**The setup.** A deterministic, tool-using support-desk environment with a
scripted oracle policy that always solves the task correctly. A fault
injector breaks exactly one thing at a known step, and every fault is
labelled by whether the customer-visible outcome still looked fine
afterward (**silent**) or visibly broke (**loud**). Five judge designs
(programmatic rules, an outcome-only LLM judge, a step-by-step rubric
judge at two model sizes, and a self-consistency ensemble) are scored
across 400 trajectories on detection, which step the fault happened at,
what kind of fault it was, calibration, and cost.

**The numbers.**

- The outcome-only judge, today's production default, catches **84% of
  loud faults** but only **45% of silent ones**, while flagging **33% of
  fully correct trajectories** as faulty.
- The step-rubric judge reaches **77% silent-fault recall with zero false
  alarms**, at **3x the cost** of the outcome-only judge.
- **No judge design reads the final reply carefully enough** to catch an
  invented promise appended to an otherwise-perfect trajectory: it evades
  the rule-based judge entirely and evades the step-rubric judge **82% of
  the time**.
- Self-consistency (asking the same judge multiple times and combining the
  answers) **triples the cost and improves nothing**.

**The pairing worth making explicit.** Zheng et al. (2023, *"Judging
LLM-as-a-Judge with MT-Bench and Chatbot Arena,"* NeurIPS 2023 Datasets
and Benchmarks track, arXiv:2306.05685) is the field's peer-reviewed,
widely cited anchor for LLM-judge limitations generally: documented
position bias, verbosity bias, self-enhancement bias, and limited
reasoning ability, alongside its own finding that strong judges like
GPT-4 reach over 80% agreement with human preferences, the same level
humans reach with each other. Put the two papers side by side: judges are
not useless, they have specific, now-measured blind spots, and the newest
of those measurements is about exactly the failure mode (silent,
trajectory-level) an outcome-only default cannot see at all.

**Applied question (syllabus's own framing), for paired discussion:**
where would an outcome-only LLM-as-judge most likely miss a real failure
in your own team's agent? Push for a specific answer naming an actual step
in their own pipeline (a tool call whose result is silently wrong but
whose downstream reply still reads fine), not a generic "it might miss
things."

---

## 3. Hands-on lab (60 min)

**Deliverable this section builds toward** (Issue 5): a working evaluation
harness with a scripted regression set, plus a scorecard covering task
success, bias probes, and PII probes for the team's own agent. Rubric row
(15 pts): *"The regression harness is reproducible and trajectory-aware,
not just final-answer accuracy, and the team reports its own weaknesses
honestly."* Second rubric row (5 pts, Ethics/privacy/safety): *"Bias probe
results and PII handling are documented and demonstrated, not just
claimed."*

**Tooling decision**: the judge is Gemini, called with a structured-output
schema for its verdict (matching this course's own established pattern
since Module 1), not free-text grading. The regression harness itself is
a plain Python script in the Module 3/4 style (print state after every
stage), not a new framework; no classical NLP stack for PII either, a
lightweight regex/pattern layer plus an LLM-based semantic pass stands in
for Presidio's NER component, matching this course's own "no classical NLP
stack" rule stated in the syllabus.

Planned build order:

1. **A scripted regression set**, a small fixed set of multi-turn
   conversations against the team's own agent, each with a known expected
   outcome, mirroring Module 3's fixed FAQ scenarios.
2. **Capture the full trajectory**, not just the final reply: every tool
   call, its arguments, and its result, alongside the reply, directly
   applying the research dive's own lesson that outcome-only misses over
   half of silent failures.
3. **A step-rubric judge**, Gemini with a structured-output schema scoring
   each captured step, not just the final answer, then a pass^k run
   (repeat each scripted scenario k times) for a real consistency number,
   not a single pass/fail.
4. **A bias probe**: the same scripted scenario, run twice, with only a
   persona/identity cue changed in the simulated user's opening turn,
   nothing else different, comparing the two trajectories' scores.
5. **A PII-leakage probe**: plant a fake PII fact across two sessions
   (reusing Module 4's own two-session harness), then check the agent
   does not leak it to a differently-scoped query, and that a forget-me
   call actually removes it, both this course's own established
   convention and the exact test the rubric's ethics row asks for.
6. **Assemble the scorecard**: pass^k consistency, the bias-probe delta,
   and the PII-probe pass/fail, one artifact, since this is also exactly
   what Module 6's defense needs on the day.

**Likely bugs to name in advance**: a regression set with only one scripted
scenario (not enough to show a real pass^k number); a judge given only the
final reply because the harness never actually captured intermediate tool
calls; a bias probe that changes more than one variable at a time,
making the delta impossible to attribute; a PII probe that checks the
memory store directly instead of checking what the agent actually says out
loud, which is the thing a real user could actually see leak.

---

## 4. Discussion and wrap (30 min)

Read the defense rubric against the team's own scorecard from today's lab,
and agree, as a team, the success criteria they will defend in Module 6.
Issue 5 checkpoint: has the harness actually run, not just been written.

---

## Sources used in these notes

- Yao, Shinn, Razavi & Narasimhan (2024), "tau-bench: A Benchmark for
  Tool-Agent-User Interaction in Real-World Domains," arXiv:2406.12045.
  https://arxiv.org/abs/2406.12045. **Named in the syllabus for this
  module's research dive.**
- Barres, Dong, Ray, Si & Narasimhan (2025), "tau2-Bench: Evaluating
  Conversational Agents in a Dual-Control Environment," arXiv:2506.07982.
  https://arxiv.org/abs/2506.07982. **Named in the syllabus for this
  module's research dive.**
- Mohammadi (2026), "trajectory-judge: What Outcome-Only LLM Judges Miss
  on Agent Trajectories," arXiv:2609.00038. https://arxiv.org/abs/2609.00038.
  Single-author preprint, under review at a NeurIPS 2026 workshop, not yet
  peer-reviewed; cited for the syllabus's own "documented blind spots of
  LLM-as-judge grading" phrase, the only source found with matching,
  concrete, ground-truth-by-construction numbers.
- Cao, Sun & Yue (2026), "From Biased Chatbots to Biased Agents: Examining
  Role Assignment Effects on LLM Agent Robustness," accepted to the AAAI
  2026 TrustAgent Workshop, arXiv:2602.12285.
  https://arxiv.org/abs/2602.12285. Cited for the bias-probing mechanism
  and its 26.2% number; a workshop paper, not a full conference paper.
- Zheng et al. (2023), "Judging LLM-as-a-Judge with MT-Bench and Chatbot
  Arena," NeurIPS 2023 Datasets and Benchmarks track, arXiv:2306.05685.
  https://arxiv.org/abs/2306.05685. Peer-reviewed anchor for general
  LLM-judge bias (position, verbosity, self-enhancement) and the
  human-agreement baseline; a supporting citation, not the research-dive
  paper.

All figures above were read directly from each paper's own arXiv abstract
page (and tau-bench's full HTML text) on 2026-09-16. Unlike Module 4's
three papers, none of these four could be saved as a local PDF into this
folder: this environment has no outbound fetch to arxiv.org's PDF endpoint,
only to its abstract/HTML pages. Whoever builds the infographics from
these notes should treat the arXiv links above as the citable source, and
add a local PDF copy to this folder if one gets downloaded outside this
environment.
