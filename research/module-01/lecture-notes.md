# Module 1 research dive: Gorilla

Scope note: Module 1's full deck predates the `lecture-notes.md`-first rule
(`PROGRESS.md`'s build order), and this document does not retroactively
cover the whole module. It exists to close the specific gap flagged in
`PROGRESS.md`'s 2026-09-16 depth-bar audit ("Row 6, cited paper, does not
apply to this module... there is no paper for this module to cite") now
that the paper-extension project model needs a real research-dive paper
per topic, Extraction included. This is the source document for the five
new "Research dive" slides in `lectures/dsca-module-01.html`, and for a
future NotebookLM concept-infographic prompt if the instructor wants one.

## Paper

Patil, Zhang, Wang & Gonzalez (2023), "Gorilla: Large Language Model
Connected with Massive APIs," UC Berkeley. Open access, arXiv:2305.15334,
CC BY 4.0. Not downloaded as a local PDF (this sandbox has no outbound
fetch to arXiv's PDF endpoint, the same standing limitation logged for
Module 5's paper track); verified against the arXiv HTML rendering
(`arxiv.org/html/2305.15334v1`), fetched and read in full, no truncation.

## Why this paper, for this module

Module 1 teaches structured intent and entity extraction via function
calling and schema-enforced structured output: the model's job is to turn
an utterance into a valid, schema-conforming call. Gorilla is the paper
that measures exactly this capability at scale, thousands of real APIs
instead of one hand-written schema, and its central finding
(hallucination, not malformed shape, is the real failure mode) is the
same lesson the module's own "schema is compiled into decoding, but that
guarantees shape, not truth" slide already teaches with one example.
Gorilla is also directly usable as an Extraction-topic project paper: it
has a real public repo (`gorilla.cs.berkeley.edu`), a released dataset
(APIBench, 11,000+ instruction-API pairs), and a clear reproduction path
(fine-tune or prompt a model, measure AST-matched accuracy and
hallucination rate against APIBench).

## The problem

LLMs, even GPT-4, are unreliable at invoking real APIs from a large,
overlapping, and changing set of tools: they generate inaccurate
arguments and hallucinate API calls that do not exist. This is distinct
from the module's own "wrong value in a valid shape" failure mode:
Gorilla's hallucination is invoking something with no match anywhere in
the real API space at all, a fabricated tool, not a wrong but real one.

The paper's own benchmark, APIBench, is built from three real API hubs:
HuggingFace (925 models, the top 20 most-downloaded per domain across
7 multimodal, 8 computer-vision, 12 NLP, 5 audio, 2 tabular, and 2
reinforcement-learning domains, out of 203,681 total models on the
platform), TorchHub (94 API calls, exhaustive), and TensorHub (696 API
calls after filtering out poorly documented ones, out of 801 in v2).
1,645 APIs total, each converted to ten synthetic instruction-API pairs
via self-instruct prompting (GPT-4 generating realistic user requests
with no API names or hints given), for 11,000+ pairs released as an
open dataset.

Zero-shot GPT-4 hallucinates 78.65% of its TensorHub API calls: it names
a tool that has no match anywhere in the real API space. GPT-3.5 does
better on this specific measure (47.88% hallucination on TensorHub), a
finding the paper itself calls "surprising" and does not fully explain,
speculating RLHF plays a role in making a model more truthful. Claude
(the `claude-v1` checkpoint tested) hallucinates 88.46% of TensorHub
calls zero-shot, the worst of the four baselines tested.

## Verifying correctness: AST sub-tree matching

Because many correct APIs exist for one task (over 40 different image
classification models, say), a test-case or exact-string match does not
work. The paper's evaluation parses the generated code into an abstract
syntax tree, then checks whether that tree is a sub-tree of any real
API's own AST in APIBench, matching on the arguments that matter (for
example `repo_or_dir` and `model` for a `torch.hub.load` call) while
allowing optional arguments like `pretrained=True` to differ. A
hallucination is defined precisely as a generated call with no matching
sub-tree anywhere in the dataset, an invented tool; an incorrect but real
API call is scored separately, as an error, not a hallucination.

## The method: retriever-aware fine-tuning

Gorilla is a fine-tuned LLaMA-7B model, trained on the self-instruct
instruction-API pairs described above, converted into a single-turn
user-agent chat format. The paper's specific contribution beyond
ordinary fine-tuning is retriever-aware training: some training examples
append the real API documentation to the prompt ("Use this API
documentation for reference: <doc>"), teaching the model to read and
follow supplied documentation at inference time rather than only
recalling API shapes memorized during training.

This buys two things the module's own schema-enforcement approach cannot,
on its own, provide: adaptation to test-time documentation changes (the
paper demonstrates Gorilla correctly following an upgraded FCN backbone,
ResNet-50 to ResNet-101, and a changed model registry, pytorch/vision to
NVIDIA/DeepLearningExamples:torchhub, without retraining, because the
current documentation is supplied at call time) and resilience to a
retriever that is not perfect (finetuning without a retriever and adding
a non-oracle one at evaluation time drops accuracy sharply, 21.50 points
in Torch Hub, 47.57 points in HuggingFace, so a bad retriever can hurt
more than it helps, a genuine and non-obvious finding worth naming rather
than glossing over).

Framing for this course, stated explicitly, not left implicit: this
course does not fine-tune models, it uses prompted function calling.
Gorilla is still the right research dive because the underlying
principle, grounding a call in real, current documentation beats relying
on a model's memorized (and often stale or hallucinated) sense of what an
API looks like, applies to a prompted call exactly as much as a
fine-tuned one. The module's own retrieval-free schema approach works
because the schema is small and fixed; Gorilla's paper is what happens
when the API surface is too large to fit in a prompt at all, and
retrieval becomes necessary rather than optional.

## Results

Zero-shot overall accuracy (Table 1, AST-matched against APIBench):
Gorilla 59.13% / 71.68% / 83.79% across TorchHub / HuggingFace /
TensorHub respectively, beating GPT-4 (38.70% / 19.80% / 18.20%) by
20.43 points overall and ChatGPT (GPT-3.5, 48.38% / 16.81% / 41.75%) by
10.75 points overall, and beating base LLaMA-7B (0% across all three,
zero-shot, with no fine-tuning) by as much as 83 points.

Hallucination reduction (the paper's headline safety claim): Gorilla's
zero-shot hallucination rate is 6.98% (TorchHub), 10.95% (HuggingFace),
and 5.40% (TensorHub), against GPT-4's 36.55% / 37.16% / 78.65% on the
same three hubs, respectively. The TensorHub column is the sharpest
single comparison: the same underlying task, GPT-4 hallucinating an
invented tool on 78.65% of attempts, Gorilla on 5.40%.

Retriever-aware training specifically (Table 2): finetuning with a
ground-truth (oracle) retriever included beats finetuning without one by
12.37 points on Torch Hub and 23.46 points on HuggingFace, when the
oracle retriever is also available at evaluation time. Constraint-aware
API selection (Table 3, choosing an API that also satisfies a stated
accuracy or parameter-count bound): Gorilla matches the best-performing
baseline, GPT-3.5, when a retriever is available, and has the highest
zero-shot accuracy among all models tested.

## Limits, stated plainly

Scoped to a single API call per request, not the multi-step tool chains
a real agentic system often needs to plan and execute. APIBench is
entirely ML-model APIs across three specific hubs, chosen because they
are richly documented and structurally comparable, not general-purpose
REST APIs with arbitrary side effects. The paper's own honest, unresolved
finding, that GPT-3.5 hallucinates less than GPT-4 in their tests, is
flagged as surprising in the text itself, with only a speculative
explanation (RLHF), not a settled one; this is a good example of a
paper naming what it does not know rather than overclaiming.

## Sources

- Patil, Zhang, Wang & Gonzalez (2023), "Gorilla: Large Language Model
  Connected with Massive APIs," arXiv:2305.15334.
  <https://arxiv.org/abs/2305.15334>
