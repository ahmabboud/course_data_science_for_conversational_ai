# Module 4: Memory — lecture notes

Written before the deck, per `PROGRESS.md`'s module build order. This is the
source the slide deck's prose gets pulled from, the source for the
concept-infographic NotebookLM prompt, and it is posted for students as
extended reading in its own right. Organised by this module's syllabus
segments (`Data Science for Conversational AI - Syllabus.docx`, Session 4):
Lecture (50 min, split here into core concepts and a research dive on one
paper), Hands-on lab (100 min), Discussion and wrap (30 min).

**Objective** (from the syllabus). Let the agent remember, across turns and
across separate sessions, without quietly becoming a privacy liability.

---

## 1. Lecture, part one: session memory vs. persistent memory (~15 min)

Every agent already has one kind of memory for free: the running list of
messages in the current conversation, held in context for as long as the
session lasts. Call this **session memory**. It costs nothing to build,
because it is just the message array the agent already passes to the model
on every turn (the same array Module 1's structured-extraction agent and
Module 2's LangGraph state already carry). It disappears the moment the
session ends: close the tab, start a new conversation, and the agent has
never met this user before.

**Persistent, cross-session memory** is the harder problem this module is
actually about: facts that survive past the session that produced them, so
that a user who left three days ago and comes back today gets an agent that
still knows their name, their open order, or the constraint they stated last
time. This is not "a bigger context window." A context window, however
large, is still bounded, still per-session by default, and still charges
per token on every single call whether or not the content in it is relevant
to the current turn. Persistent memory is a separate store, written to
between sessions, read from selectively at the start of a new one.

The field has converged on two working patterns for building that store,
named directly in this module's reading: the **extract-and-update pattern**
(the shape Mem0 implements) and the **temporal-knowledge-graph pattern** (the
shape Zep implements, via its Graphiti engine). They differ in what a
"memory" is shaped like and in how they handle a new fact that contradicts an
old one. Both are covered below at the level of their own published
technical reports, not a marketing description.

### 1.1 The extract-and-update pattern (Mem0)

Mem0's own technical report (Chhikara et al., 2025, *"Mem0: Building
Production-Ready AI Agents with Scalable Long-Term Memory,"* arXiv:2504.19413)
describes a pipeline with three stages, run every time new conversation
turns arrive:

1. **Retrieve candidates.** Embed the new messages, run a vector search
   against the existing memory store scoped to this `user_id` (or
   `agent_id`/`run_id`), and pull back the memories that might need to
   change because of what was just said.
2. **Decide, per fact.** One LLM call compares the new information against
   each retrieved candidate and issues one of four verdicts: `ADD` (this is
   new, nothing like it exists yet), `UPDATE` (this replaces or refines an
   existing memory), `DELETE` (this contradicts and invalidates an existing
   memory), or no-op (nothing worth storing changed). This is the
   mechanism worth opening up for students: memory is not a log that only
   grows, it is a store that gets actively reconciled against what already
   exists, one fact at a time.
3. **Enrich for retrieval.** Named entities (people, places, organizations)
   get extracted from memory text; shared entities between memories boost
   related results at search time, which is the paper's graph-memory
   variant taken to its logical conclusion even in the non-graph base
   configuration.

**Cost, stated, not implied.** Against a full-context baseline (concatenate
the entire conversation history into every call), Mem0 reports a 91% lower
p95 latency and more than 90% lower token cost on its LOCOMO benchmark runs,
while its LLM-as-a-Judge accuracy is 26% relatively higher than an OpenAI
memory baseline evaluated the same way. The mechanism this trades away is
exactly what the retrieve-then-decide step above buys back: instead of
paying for every past token on every future call, you pay once, up front,
per new fact, to decide whether it belongs in the store at all.

### 1.2 The temporal-knowledge-graph pattern (Zep / Graphiti)

Zep's technical report (Rasmussen, Paliychuk, Beauvais, Ryan & Chalef, 2025,
*"Zep: A Temporal Knowledge Graph Architecture for Agent Memory,"*
arXiv:2501.13956) represents memory as a graph rather than a flat store of
facts. The unit of ingestion is an **Episode** (a message, a text blob, or a
JSON record); episodes get processed into **entity nodes** and **semantic
edges** between them, an edge being a fact like *(user, prefers, aisle seat)*.

The formalism worth putting in front of students directly is the **bi-temporal
model**: every edge carries not one timestamp but two independent timelines.
Timeline *T* is when the fact was actually true in the world (`t_valid`,
`t_invalid`); timeline *T′* is when Zep's own database learned about it
(`t′_created`, `t′_expired`). A fact can be true from last Tuesday but only
entered the graph today; a fact can stop being true next week without the
system needing to have known that in advance. This is the specific thing a
flat key-value memory store cannot represent: it can hold "user's preferred
seat is aisle," but it cannot hold *both* "true starting last Tuesday" *and*
"the system found this out today, three days late," and it has no principled
way to represent a fact's expiry at all short of deleting the row.

**Edge invalidation, the mechanism a black box hides.** When a new edge
comes in, an LLM call compares it against semantically related existing
edges to check for a temporally overlapping contradiction (e.g., a new
"user's preferred seat is window" against the older aisle-seat edge). If one
is found, the old edge is not deleted, it is invalidated: its `t_invalid` is
set to the new edge's `t_valid`, and the transactional timeline `T′` always
prioritises the newer information for that decision. The history is kept,
not erased, which is the property a temporal graph buys over a flat store
that would just overwrite the old value.

**Cost and a critical read.** Zep reports 94.8% accuracy on the Deep Memory
Retrieval (DMR) benchmark against MemGPT's 93.4%, and up to an 18.5% accuracy
gain with a 90% latency reduction on the harder LongMemEval benchmark. Worth
saying to students plainly, because the paper says it about its own headline
number: DMR's 500 conversations average only 60 messages each, comfortably
inside a modern context window, and a full-conversation baseline (no memory
system at all) scores 94.4%, nearly matching Zep on that same benchmark. The
paper's own stated critique of its easier benchmark is a good model for the
kind of critical read this course expects of any single paper's headline
result, including the one in the research dive below.

### 1.3 Summarization and compaction for long conversations (~10 min)

Neither pattern above eliminates the need to keep a *session's own*
in-context history from silently overflowing the window as a conversation
runs long. Two shapes exist for compacting it down:

- **Rolling / recursive summarization.** After every session (or every *k*
  turns), replace the raw turns with an updated summary that folds the new
  turns into the previous summary: `summary_t = LLM(summary_{t-1}, turns_t)`.
  Cheap, but lossy in a specific way: information not represented in the
  running summary is gone for good the next time it recurs, and a
  summarization pass itself can introduce error that compounds over many
  rounds.
- **Hierarchical / segment-level compaction**, the shape this module's
  research-dive paper actually builds on. Rather than summarizing turn by
  turn, first **segment** the conversation into topically coherent chunks,
  then compress *within* a segment rather than across the whole history.
  This is a genuinely different mechanism from rolling summarization: it
  changes the *unit* memory operates on (a topic segment, not a turn or an
  entire session) before it ever compresses anything.

Both are legitimate; the field has not converged on one. What is not a real
choice is silently truncating (dropping the oldest turns with no compaction
at all): that is the specific failure this module's lab exists to prevent,
and it is graded directly (this module's rubric row: *"long conversations
are compacted rather than silently truncated or overflowed"*).

### 1.4 What persistent memory costs in privacy risk (~5 min, previews Module 5)

A memory store that persists across sessions is, definitionally, a store of
personal data that outlives the interaction that produced it. Three costs
that a working system has to actually answer, not just acknowledge:

- **Retention.** How long does a fact live before it expires on its own?
  Zep's bi-temporal model gives a *mechanism* for expiry (`t_invalid`); it
  does not by itself give a *policy* for how long is appropriate, that is a
  product decision this module's lab asks each team to make explicitly.
- **The right to be forgotten.** A user asking the agent to forget something
  is not an edge case, it is a requirement: can the system actually delete
  (not just stop displaying) a specific fact about a specific user, and can
  it prove it did? This is this module's discussion-and-wrap topic, below.
- **What gets stored at all.** Extracting "salient information" (Mem0's own
  phrase) from a conversation means deciding what counts as salient; a
  system that over-extracts (storing a health condition mentioned in
  passing, a location, a relationship) has created a PII liability whether
  or not it was ever asked to. Module 5's bias-and-PII scorecard is where
  this gets measured; this module is where the design decision gets made.

---

## 2. Research dive: SeCom (Pan et al., ICLR 2025) (~20 min)

**Paper.** Pan, Wu, Jiang, Luo, Cheng, Li, Yang, Lin, Zhao, Qiu & Gao (2025),
*"On Memory Construction and Retrieval for Personalized Conversational
Agents,"* published as a conference paper at ICLR 2025. Open access on arXiv
(`2502.05589`). This is the exact reading named in the syllabus for this
module, downloaded to `research/module-04/pan-2025-secom-memory.pdf`.

### 2.1 The idea

Existing memory systems build their memory bank at one of two fixed
granularities: **turn-level** (one memory unit per user-agent exchange) or
**session-level** (one memory unit per entire conversation session). The
paper's central claim is that granularity itself is the lever nobody had
tuned: turn-level units are too small to carry topical context, session-level
units are too large and dilute retrieval with irrelevant content from the
same session. Its proposed method, **SeCom**, introduces a third granularity,
the **segment**: a topically coherent span of consecutive turns, found by a
conversation-segmentation model rather than fixed in advance.

### 2.2 The formalism

The paper states its framework precisely. Let conversation history
`H = {c_i}` be a set of sessions, each session `c_i = {t_j}` a sequence of
turns. Memory construction builds a bank `M` from `H`; for a turn-level bank
each memory unit is one turn, `|M| = sum(T_i)`; for a session-level bank
each unit is one session, `|M| = C`. Retrieval takes a target request `u*`
and a context budget `N`, and returns the `N` most relevant units,
`{m_n} ← f_R(u*, M, N)`; response generation conditions on those units in
time order.

SeCom changes what a unit *is*: it first runs a segmentation model `f_I`
that partitions each session `c_i` into `K_i` topical segments, so
`|M| = sum(K_i)`, each memory unit now a segment rather than a turn or a
session. It then applies a **compression-based denoising** step before
retrieval: `{m_n} ← f_R(u*, f_Comp(M), N)`, where `f_Comp` is LLMLingua-2 (Pan
et al., 2024), a prompt-compression model, used here specifically to strip
redundant natural-language padding out of each memory unit before it
competes for a retrieval slot. This is the paper's second finding, separate
from segmentation: denoising by compression measurably improves retrieval
accuracy at every granularity it was tried on, not just at the segment
level SeCom introduces.

### 2.3 The experiment

Two primary benchmarks: **LOCOMO** and **Long-MT-Bench+**, both built for
long-term, multi-session dialogue. Baselines compared against: Zero History
(no memory at all), Full History (concatenate everything), Turn-Level and
Session-Level (with both BM25 and MPNet-based retrieval), and three
summarization-family systems from prior work, SumMem, RecurSum, and
ConditionMem, plus MemoChat. Metrics: GPT4Score (GPT-4 rates the response
0-100 against a reference), BLEU, ROUGE-1/2/L, and BERTScore, alongside the
actual context length in tokens each method needed to reach its score, a
genuine cost/quality tradeoff table rather than accuracy reported alone.

### 2.4 The results

On LOCOMO, SeCom (BM25 retrieval, GPT-4 segmentation) reaches a GPT4Score of
**71.57**, ahead of Session-Level/BM25 (63.16), Turn-Level/BM25 (65.58), and
Full History (54.15, despite Full History using nearly four times the
context: 13,330 tokens against SeCom's 3,731). On Long-MT-Bench+, SeCom
(MPNet retrieval, GPT-4 segmentation) reaches 88.81 against Turn-Level/MPNet's
84.91 and Session-Level/BM25's 81.27. The paper also shows the segmentation
model itself does not have to be GPT-4: swapping in Mistral-7B or a small
RoBERTa-based segmenter keeps most of the advantage over the granularity
baselines, which is the paper's own answer to "this only works because it
spent a fortune on segmentation."

### 2.5 The limits, read critically

The paper is explicit about one limitation and understates a second, worth
raising exactly this way with students, the same shape as Module 3's
research dive:

- **Stated by the authors.** Segmentation quality still bounds everything
  downstream of it: a badly segmented conversation produces memory units
  that are exactly as incoherent as a badly chunked document was in Module
  3's research dive, the paper's own ablation against Mistral-7B and
  RoBERTa segmenters shows a real, if smaller, accuracy gap opening up
  against the GPT-4 segmenter.
- **A tension worth adding.** The context budget in the main results table
  is fixed at 4k tokens for LOCOMO and 1k tokens for Long-MT-Bench+ across
  every method compared, which is a fair way to compare retrieval quality
  at equal cost, but it also means the paper never actually reports what
  happens as the budget itself is varied per method; a system willing to
  spend more tokens than SeCom's 3,731 (but still far under Full History's
  13,330) is untested territory the table does not cover.

**Applied question for the lab**: does the segment-level pattern actually
help a team's own two-to-three-person agent, whose conversation history is
nowhere near LOCOMO's scale, or is the fixed-cost extract-and-update pattern
(section 1.1) the better fit for a small, bounded memory store the way CAG
was the better fit for a small, bounded knowledge base in Module 3? Students
should be able to argue either side using this module's own numbers.

---

## 3. Hands-on lab (100 min)

**Deliverable this section builds toward** (Issue 4, this module's syllabus
deliverable): *the team's agent demonstrably remembers a specific user
across two separate sessions, with a working compaction strategy for long
conversations.* Rubric row (15 pts): *"The agent correctly recalls a specific
user across two separate sessions, and long conversations are compacted
rather than silently truncated or overflowed."*

**Tooling decision for this module's demo and lab** (confirmed with the
instructor): build both memory patterns from scratch, plain Python plus the
one shared Gemini client every other module's demo already uses, no new
heavy dependency (no vector database service, no graph database, no Mem0 or
Zep SDK installed). This matches Module 3's precedent (`grounded_rag.py`
built hybrid search and reranking from scratch rather than installing a
vector store): the lecture above names and cites the real, production
systems accurately; the lab and demo build the mechanism directly so
students see exactly what is inside it, at the cost of not being
production-grade themselves.

Planned build order (mirrors Module 3's walkthrough shape):

1. **A minimal memory store.** A plain list of structured facts
   (`{text, user_id, created_at, valid, superseded_by}`), stored to a local
   file or SQLite table so it survives past the process exiting, which is
   what makes it persistent rather than session memory.
2. **The extract-and-update step.** One LLM call per new turn (or per
   session-end) that compares candidate facts against the existing store
   (a simple keyword or embedding-similarity retrieval is enough at this
   scale) and returns an `ADD` / `UPDATE` / `DELETE` / no-op verdict per
   fact, directly implementing section 1.1's pattern.
3. **A minimal temporal fact, as a stretch goal.** Rather than a full graph
   database, represent the bi-temporal idea directly on the flat store: a
   fact row carries `valid_from` and `superseded_by` (pointing at the row
   that invalidated it), so a team can demonstrate section 1.2's core
   insight, that an old fact is invalidated rather than silently
   overwritten, without standing up Graphiti itself.
4. **Recognizing a returning user across two sessions.** The actual checkpoint
   for Issue 4: run the agent, end the process, start it again as a "new"
   session, and show it recalls a fact from the first run.
5. **Summarization / compaction.** A token-budget trigger that, once a
   session's own in-context history crosses a threshold, replaces the
   oldest turns with a rolling summary (section 1.3) rather than letting the
   context window silently overflow or truncate.

**Likely bugs to name in advance** (same convention as Module 3's lab-brief
slide): a memory store with no `user_id` scoping that leaks one user's facts
into another's session; an extract-and-update step that never actually
issues `DELETE` or `UPDATE` (only ever `ADD`s), silently accumulating
contradictory facts forever; a compaction trigger that fires so late the
context window has already overflowed before it runs.

---

## 4. Discussion and wrap (30 min)

**Memory failure modes**, the module's actual discussion topic:

- **Stale facts.** A fact that was true and got stored, then stopped being
  true, but nothing ever invalidated it. This is exactly what section 1.2's
  edge-invalidation mechanism exists to prevent, and exactly what a naive
  extract-and-update implementation risks if its `UPDATE`/`DELETE` verdicts
  are unreliable.
- **Wrong recall.** Retrieval surfaces a real, once-true fact at the wrong
  time, most commonly when an old and a new fact about the same thing both
  remain in the store and the wrong one gets ranked first. Ask directly:
  is this a retrieval-ranking bug, or a failure to invalidate the old fact
  in the first place? The two failures look identical to a user and need
  different fixes.
- **The user asks the agent to forget something.** Not a hypothetical: a
  real system has to support actual deletion of a specific fact about a
  specific user, on request, and a team should be able to demonstrate it,
  not just claim the store supports it in principle.

**Before Module 5**: this module's reading (SeCom, plus Mem0 and Zep
documentation) previews Module 5's evaluation and responsible-deployment
focus directly, a memory system that stores more than it should is exactly
the kind of PII liability Module 5's bias-and-PII scorecard is built to
catch. Issue 4 checkpoint due before that module begins.

---

## Sources used in these notes

- Pan, Wu, Jiang, Luo, Cheng, Li, Yang, Lin, Zhao, Qiu & Gao (2025), "On
  Memory Construction and Retrieval for Personalized Conversational Agents,"
  ICLR 2025. `research/module-04/pan-2025-secom-memory.pdf`. **This
  module's research-dive paper.**
- Chhikara, Khant, Aryan, Singh & Yadav (2025), "Mem0: Building
  Production-Ready AI Agents with Scalable Long-Term Memory," arXiv:2504.19413.
  `research/module-04/chhikara-2025-mem0.pdf`. Cited for the extract-and-update
  pattern and its cost numbers; not the research-dive paper, a supporting
  citation for the working-example the syllabus names.
- Rasmussen, Paliychuk, Beauvais, Ryan & Chalef (2025), "Zep: A Temporal
  Knowledge Graph Architecture for Agent Memory," arXiv:2501.13956.
  `research/module-04/rasmussen-2025-zep-graphiti.pdf`. Cited for the
  temporal-knowledge-graph pattern, its bi-temporal formalism, and its own
  critique of the DMR benchmark; likewise a supporting citation, not the
  research-dive paper.

All figures above were read directly from these three PDFs on 2026-09-15,
not reconstructed from memory or from marketing pages; page-level citations
for each numbered claim are in the PDFs' own Table 1 (SeCom), abstract and
Section 4.2 (Zep), and abstract (Mem0).
