# Project paper and repo menu

This is the curated menu `PROJECT-REDESIGN.md` and Module 1's kickoff slide
both point to: for each of the course's five project topics, one or more
papers that already have a real, working, public repository, so a team can
start reproducing a baseline on day one instead of writing one from
scratch. Every entry below was checked directly (arXiv listing plus the
repository's own README) on 2026-09-17. A team is not limited to this
list. Self-proposed papers are equally valid, subject to the same
idea-pitch approval step and the same compute and cost cap, whether or not
they have a repo; this menu exists to make the fast, low-risk starting
point obvious, not to be the only option.

**The compute and cost cap, restated:** must run on a personal computer,
or no more than $20 of total API spend. A smoke test standing in for
full-scale validation is fine, as long as the team can explain what
full-scale validation would actually require.

## Extraction (Module 1)

### Gorilla, taught in this module's own research dive
Patil, Zhang, Wang and Gonzalez (2023), arXiv:2305.15334.
Repo: `github.com/ShishirPatil/gorilla` (Apache 2.0, active).

A team does not need to retrain Gorilla from scratch. The repo ships
released checkpoints (LLaMA and OpenFunctions variants) on Hugging Face,
so reproduction is inference against a subset of APIBench, run on a
laptop GPU or a free-tier hosted notebook, no training run required.
Extension ideas the paper leaves open: a new API category APIBench does
not cover, an ablation on retriever quality, or a tighter hallucination
check than AST sub-tree matching alone.

### ToolLLM / ToolBench
Qin, Liang, Ye, Zhu, Yan, Lu, Lin, Cong, Tang, Qian, Zhao, Hong, Tian, Xie,
Zhou, Gerstein, Li, Liu and Sun (2023), arXiv:2307.16789, ICLR 2024
spotlight. Repo: `github.com/OpenBMB/ToolBench` (active).

3,451 tools across 16,464 real APIs, an order of magnitude larger than
APIBench, with a released ToolLLaMA checkpoint. Reproduction on a small
query subset (not the full 16k-tool suite) keeps API spend for any
GPT-family comparison baseline well under the cap. Good fit for a team
that wants to extend tool selection or retrieval at a larger tool-catalog
scale than Gorilla's.

## Dialogue (Module 2)

### Helping Customers in Distress, taught in this module's own research dive
Atreya, Wanger, Batra, Hankache, Iglesias Jr, Sinclair, Pelosio, McMillan,
Cowan and Khraishi (2026), arXiv:2605.16268.
**No public repository found.** This is a real production deployment at a
bank, not an open-source release; nothing on arXiv, the authors' pages, or
a search of the usual code-hosting sites turned one up. Still valid as
required background reading and as a topic anchor, but a team choosing to
extend it is choosing to build the triage-agent baseline from the paper's
own description with no reference implementation, which is real extra
work up front. The two entries below are the repo-backed alternatives for
teams that want a faster start on the same topic.

### MultiWOZ
Budzianowski, Wen, Tseng, Casanueva, Ultes, Ramadan and Gasic (2018),
arXiv:1810.00278, EMNLP 2018. Repo: `github.com/budzianowski/multiwoz`
(active, MultiWOZ 2.0 through 2.2 included).

10,000+ human-human, multi-domain task-oriented dialogues with a working
dialogue-state-tracking baseline, runs on a laptop CPU, no API spend
required at all if the baseline model is used as is. A team could extend
it with an LLM-based state tracker, or add a routing and escalation layer
that this dataset's original baselines do not attempt.

### ABCD (Action-Based Conversations Dataset)
Chen, Chen, Su, Peng, Chen, Wang, Yu (2021), arXiv:2104.00783.
Repo: `github.com/asappresearch/abcd` (active).

The closest thematic match to this module's own routing-and-escalation
teaching: 10,000+ dialogues where an agent must balance what the customer
wants against company policy, with two built-in tasks (Action State
Tracking, Cascading Dialogue Success). Baselines run on a laptop or a
single modest GPU, no API spend required for the released baselines. A
strong fit for a team that wants to build an LLM agent that follows
guideline-constrained workflows and compare it against this dataset's own
non-LLM baselines.

## Grounding (Module 3)

### Cache-Augmented Generation ("Don't Do RAG"), taught in this module's own research dive
Chan, Chen, Cheng and Huang (2024), arXiv:2412.15605, WWW '25 short paper.
Repo: `github.com/hhhuang/CAG` (active).

Cheapest reproduction on this whole menu: preload a knowledge source into
an open model's context and cache it, no retrieval index, no training, no
per-query API cost beyond the model calls themselves. Runs on a personal
computer with a small open model. Extension ideas: a hybrid CAG-plus-RAG
fallback for knowledge sources too large to fit in context (the paper's
own stated limit), or a cache-eviction policy for a changing knowledge
base.

### Self-RAG
Asai, Wu, Wang, Sil and Hajishirzi (2023), arXiv:2310.11511, ICLR 2024
oral. Repo: `github.com/AkariAsai/self-rag` (active).

Released 7B and 13B checkpoints mean a team reproduces by running
inference, not training; a quantized 7B model is workable on a single
consumer GPU or a free-tier hosted notebook. Retrieves on demand rather
than every turn, and self-critiques its own output, a different mechanism
from this module's own RAG-versus-CAG contrast, so it extends the
module's teaching rather than repeating it. Extension ideas: swap in a
different retrieval index or domain, or adapt the reflection-token scheme
to a task Self-RAG was not evaluated on.

## Memory (Module 4)

### Mem0, taught in this module's own research dive
Chhikara, Ranganathan, Chhaya, Behrooz, Mohapatra, Rich, Rao and Chandar
(2025), arXiv:2504.19413. Repo: `github.com/mem0ai/mem0` (active,
production-maintained).

A `pip install` and an LLM API key, runs on a laptop, cheap: the demo
already built for `demos/module-04/memory_demo.py` is proof this fits the
cap comfortably. Extension ideas: a domain-specific memory schema, a
different conflict-resolution policy than the library's current additive
behavior, or a retrieval-quality comparison against Zep or SeCom below.

### Zep / Graphiti, taught in this module's own research dive
Rasmussen, Plenz, Fadeeva, Meissner, Talenko and Chalef (2025),
arXiv:2501.13956. Repo: `github.com/getzep/graphiti` (active).

Self-hostable with a graph database (Neo4j or FalkorDB) via Docker on a
personal computer, plus an LLM API key for entity and edge extraction; a
smoke-scale knowledge graph fits the cap. Extension ideas: a custom entity
or edge ontology for a specific domain, or a temporal-decay policy for
facts that go stale, an open question the library's own issue tracker
flags as unresolved.

### SeCom, taught in this module's own research dive
Pan, Wu, Jiang, Luo, Cheng, Li, Yang, Lin, Zhao, Qiu and Gao (2025),
arXiv:2502.05589, ICLR 2025. Repo: `github.com/microsoft/SeCom`
(official, Microsoft Research).

Segment-level memory construction plus compression-based denoising,
evaluated on the LOCOMO and Long-MT-Bench+ benchmarks; a subset of either
benchmark is a reasonable smoke test within the cap (embeddings plus a
modest number of LLM calls). Extension ideas: a different segmentation
signal than the paper's topic-shift model, or a denoising method other
than LLMLingua-2.

### MemGPT / Letta, not currently taught
Packer, Wooders, Lin, Fang, Patil, Stoica and Gonzalez (2023),
arXiv:2310.08560. Repo: `github.com/letta-ai/letta` (the project renamed
itself from MemGPT to Letta in 2024; the original `cpacker/MemGPT` repo
now redirects there, still active and heavily maintained).

The paper that made "an LLM as an operating system managing its own
context" a mainstream idea, predating and distinct from both Mem0's
extract-and-update pattern and Zep's temporal graph. Self-hostable, an
LLM API key covers the cost, fits the cap easily. Included specifically
because none of this module's three taught papers use this mechanism, so
a team picking it is deliberately choosing the road not covered in
lecture. Extension ideas: a new memory-tier eviction policy, or a
head-to-head comparison against Mem0 or Zep on the same task.

## Evaluation (Module 5)

### tau-bench, taught in this module's own research dive
Yao, Shinn, Razavi and Narasimhan (2024), arXiv:2406.12045.
Repo: `github.com/sierra-research/tau-bench` (active).

A team does not need to run the full task suite across every domain to
reproduce something meaningful; a handful of tasks in one domain (retail
or airline) with a cheaper model keeps API spend well under $20. Extension
ideas: a new domain policy file, or a different simulated-user strategy
than the paper's own.

### tau2-bench, taught in this module's own research dive
Barres, Dong, Ray, Si and Narasimhan (2025), arXiv:2506.07982.
Repo: `github.com/sierra-research/tau2-bench` (active, includes a
knowledge-retrieval banking domain and voice evaluation, both newer than
the paper this course reads).

Same reproduction shape as tau-bench: a task subset in one domain, a
cheaper model, comfortably inside the cap. Its dual-control model (the
user can act too, not just talk) is the module's own teaching point, so
an extension that adds a new user-action type or a new coordination
failure mode to probe for is a direct continuation of the lecture.

### AgentBench, not currently taught
Liu, Yu, Zhang, Zhang, Cheng, Zhang, Dong, Tang (2023), arXiv:2308.03688,
ICLR 2024. Repo: `github.com/THUDM/AgentBench` (active).

Eight evaluation environments, several of them (knowledge-graph
question-answering, database operations) run comfortably on a personal
computer with a modest API budget; the heavier ones (operating-system,
web-browsing) are better avoided under the cap unless a team scopes to a
single lightweight environment. Included as the broader, non-Sierra
alternative for a team that wants to evaluate general agent capability
rather than one customer-service simulation.

## How to read this menu against the idea-pitch step

Naming a paper here is not the same as an approved pitch. The idea-pitch
step still applies to every team regardless of which paper they pick:
one paragraph, submitted before real work starts, describing the intended
extension specifically enough that the instructor can check it is not
already someone else's published follow-up. A repo-backed baseline just
means less of that team's own time goes to standing up the baseline
before they can start on the part that is actually theirs.
