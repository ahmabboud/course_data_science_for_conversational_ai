# Module 2 research dive: Helping Customers in Distress

Scope note: same situation as `research/module-01/lecture-notes.md`.
Module 2's full deck predates the `lecture-notes.md`-first rule, and this
document does not retroactively cover the whole module. It exists to
close the gap `PROGRESS.md`'s 2026-09-16 depth-bar audit flagged ("Row 6
does not apply to this module... no Research dive segment in this
module's row") now that Dialogue is one of the five paper-extension
project topics and needs its own research-dive entry point. This is the
source document for the five new "Research dive" slides in
`lectures/dsca-module-02.html`.

## Paper

Atreya, Wanger, Batra, Hankache, Iglesias Jr, Sinclair, Pelosio,
McMillan, Cowan & Khraishi (2026), "Helping Customers in Distress: An
LLM-powered Agent that Converses, Probes, and Routes." Open access,
arXiv:2605.16268, CC BY 4.0, `cs.HC`. Not downloaded as a local PDF (same
standing arXiv-PDF-endpoint limitation as every module since Module 5);
verified against the arXiv HTML rendering (`arxiv.org/html/2605.16268v1`),
fetched and read in full, a short paper, no truncation.

## Why this paper, for this module

Module 2 teaches exactly one multi-agent pattern on purpose: a router
that sends a turn to a specialist path or escalates it to a human, and
explicitly avoids general multi-agent orchestration because of
coordination overhead and emergent failure modes (the module's own
assigned reading, Anthropic's "Building Effective Agents," makes this
case). This paper is a production deployment of precisely that shape,
at a bank, on fraud, scam, and dispute cases, with real measured
accuracy, handoff precision and recall, and guardrail numbers, not a
lab toy. It is also directly usable as a Dialogue-topic project paper:
it is recent, on-topic, and its measurement pattern (accuracy gain over
a baseline, handoff precision and recall, human-versus-automated
evaluation agreement) is straightforward for a student team to adapt to
a smaller domain and reproduce at a compute scale that fits the course's
own cap.

## The problem

Banks receive millions of fraud, scam, and disputed-transaction reports
a year, a volume that is rising (UK fraud reports up over 10% year on
year, per the paper's own cited source). The existing process is manual:
menu-based phone trees (IVR) and human triage, both slow and stressful
for customers and staff, and prone to misrouting a case to the wrong
specialist team. Effective triage matters on both sides of the
interaction: for customers, it means cases routed swiftly and
accurately, fewer repeat contacts and less frustration; for the bank, it
means fewer manual handoffs and misdirected workloads, freeing staff for
genuinely complex investigations.

## The architecture

Three components, each with one job, the same discipline as this
module's own router/specialist/escalation split:

- **Triage agent.** Conducts multi-turn conversations, asks targeted
  questions, classifies the case as Fraud, Scam, Dispute, or Inconclusive.
  Built via prompt engineering across third-party LLMs (Claude, Gemini,
  GPT), deliberately not fine-tuned, for policy compliance, flexibility,
  and reduced data risk. Its prompt manager orchestrates sub-prompts for
  Role, Instructions, Workflow, and Don'ts, encoding the bank's internal
  policy directly into the conversation, not as a separate check
  afterward.
- **Handoff (escalation) agent.** Detects when to end the automated chat
  and route the customer to an alternative channel, for example a direct
  phone line to a specialist team: when the customer asks to end the
  conversation, or when a vulnerability indicator is present. Measured
  separately from the triage classification itself, using a set of
  conditional trigger phrases and per-scenario success rates.
- **Guardrail agents.** Layered input and output filtering: AWS Bedrock's
  foundational content filtering, plus custom controls blocking
  unauthorized product requests, probing for internal process details,
  and non-English messages. Stress-tested with a dedicated automated
  pipeline (thousands of adversarial and benign prompts) and an internal
  red-teaming exercise simulating chat-history injection, code
  manipulation, and attempts to extract internal reasoning.

This is a genuinely useful architectural contrast for the module: the
handoff decision is its own agent with its own measured precision and
recall, not a fallback branch inside the same call that classified the
case, which is a stricter, more auditable version of "the router decides,
it never answers" than the lecture's own single-router example shows.

## The evaluation

The paper cannot ethically run large-scale live experiments against
real, distressed fraud victims to tune a triage agent, so it builds two
complementary evaluation legs:

- **Digital twins.** Synthetic customer agents built from real historical
  telephony transcripts (paired with transaction records from legacy case
  data), implemented with the OpenAI Agent SDK, simulating realistic,
  labelled, multi-turn dialogues at scale (around 3,000 transcript-based
  cases). Fidelity checks confirmed synthetic utterances mirrored real
  customer conversations.
- **Human and automated evaluation.** Subject-matter experts (SMEs) rated
  live agent conversations across three testing rounds on ten metrics
  (satisfaction, empathy, compliance, factuality, summary,
  acknowledgement, relevancy, language ease, frustration, smoothness).
  An automated pipeline using GPT-4.1 as an LLM-as-judge scored the same
  kinds of conversations at scale, with human/automated agreement
  measured explicitly: 79 to 92% on objective criteria (compliance,
  factuality, relevance, summary), only around 60% on subjective ones
  (empathy, frustration). The paper's own conclusion, stated plainly:
  automated evaluation is dependable for content-focused criteria, less
  so for subjective ones, so production deployment needs targeted
  human-in-the-loop review for emotionally nuanced cases.

This is a direct, concrete precedent for Module 5's own "know where your
judge is unreliable" lesson, worth flagging forward if there is time in
the research-dive slides.

## Results

Table 1 (relative classification-accuracy gain over the legacy IVR
system, across five LLMs, synthetic-customer testing): Claude Sonnet 3
+20.0% [16.0, 23.8], Gemini-1.5-Pro +28.4% [24.8, 31.4], GPT-4.1-mini
+21.3% [17.5, 25.9], GPT-4.1 +27.7% [26.5, 33.2], GPT-5 +30.6% [27.1,
33.9] (bracketed values are 95% confidence intervals). SME-led testing
(a smaller, human-run sample) showed a +16.0% accuracy improvement over
the legacy baseline, a real but more conservative number than the
large-scale synthetic result, worth naming so a team does not quote only
the larger figure.

Key operational metrics (compliance, satisfaction, summary) consistently
exceeded a 75-80% threshold in SME testing. Handoff precision and recall
both exceeded 90% across key handoff scenarios: the escalation agent
reliably triggers when it should, and does not over-trigger on cases
that do not need a human. Guardrails: input guardrails detected prompt
injection and hate speech at over 98% accuracy; output guardrails
identified hallucinated content at over 95% accuracy (both figures for
the GPT-4.1 variants specifically).

## Limits, stated plainly

Every reported gain is relative to a single, specific legacy baseline
(the bank's own existing IVR and manual-triage system), not to a
zero-automation or human-only baseline measured independently; the paper
frames its own contribution this way and does not claim a
universal accuracy number. The digital-twin evaluation, while carefully
validated for fidelity, is still synthetic, not live customer traffic;
the SME-tested +16.0% figure is the more conservative, human-validated
number and is meaningfully lower than the synthetic-testing figures, a
gap the paper reports rather than smooths over. Subjective-metric
agreement between human and automated judges (~60%) is explicitly named
as a current weakness, not resolved in this paper. The system is
deployed in one regulated domain (UK banking fraud/scam/dispute triage);
the paper makes no claim about transfer to a materially different
domain.

## Sources

- Atreya, Wanger, Batra, Hankache, Iglesias Jr, Sinclair, Pelosio,
  McMillan, Cowan & Khraishi (2026), "Helping Customers in Distress: An
  LLM-powered Agent that Converses, Probes, and Routes," arXiv:2605.16268.
  <https://arxiv.org/abs/2605.16268>
