"""Module 3: hybrid search, reranking, citation, and the refusal path.

Used in lectures/dsca-module-03.html: slide 3 (hybrid search), slide 4
(reciprocal rank fusion), slide 6 (reranking), and slide 8 (citation and
the refusal path) in the Lecture section, and slides 18, 19, 21, and 22
(the matching build walkthroughs) in the Hands-on lab. Run directly:

    python grounded_rag.py

Prints the pipeline's state after every stage, for three example questions,
so you see exactly what each stage actually changes: a BM25-favoring
question, a paraphrased question that needs vector search to find, and a
question the source material genuinely does not cover.

This file builds a small, fake FAQ knowledge base in memory (six short
entries, see FAQ below) and runs it through the full pipeline the lecture
describes: BM25 plus vector search, merged by reciprocal rank fusion,
narrowed by a reranking pass, then either answered with a citation or
refused, depending on whether the top passages actually address the
question. Swap FAQ for your team's own source material, the pipeline shape
around it does not change.

On reranking: a production system often uses a dedicated cross-encoder
model for this second pass. This demo reranks with one more Gemini call
instead, scoring each candidate against the query, so the whole file only
depends on the same google-genai client every other demo in this course
already uses, not a new model-serving dependency (sentence-transformers,
torch) just for one pass. The concept the lecture teaches, a second, more
careful pass over a small shortlist, is the same either way.
"""

import json
import os
import re
import time
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from google import genai
from rank_bm25 import BM25Okapi

DEMO_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(DEMO_ROOT / ".env")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Keep Module 3 independent from the shared model used by other demos. The
# default is a currently supported Flash model; override it in demos/.env
# only if a later model change requires it.
GENERATION_MODEL = os.getenv("M03_GENERATION_MODEL", "gemini-3.6-flash")
EMBEDDING_MODEL = "gemini-embedding-001"

# The fake knowledge base. Six short entries, each with a stable source_id,
# the same "which document, which section" idea the lecture's citation
# walkthrough describes. Deliberately small and in memory: the point of this
# demo is the pipeline, not a real document store.
FAQ = [
    {
        "source_id": "faq.md#shipping",
        "text": "Standard shipping within the country takes 3 to 5 business "
        "days. Expedited shipping takes 1 to 2 business days for an "
        "additional fee. Orders placed after 3pm ship the next business day.",
    },
    {
        "source_id": "faq.md#returns",
        "text": "Items may be returned within 30 days of delivery for a full "
        "refund, provided the item is unused and in its original packaging. "
        "Sale items are final and cannot be returned.",
    },
    {
        "source_id": "faq.md#warranty",
        "text": "All electronics carry a 1-year manufacturer warranty "
        "covering defects in materials and workmanship. Warranty does not "
        "cover accidental damage, water damage, or normal wear and tear.",
    },
    {
        "source_id": "faq.md#gift-cards",
        "text": "Gift cards do not expire and carry no fees. Gift cards "
        "cannot be returned or redeemed for cash, except where required by "
        "law. Lost or stolen gift card codes cannot be replaced.",
    },
    {
        "source_id": "faq.md#international",
        "text": "International orders typically arrive within 7 to 14 "
        "business days. The customer is responsible for any customs duties "
        "or import taxes charged by their country.",
    },
    {
        "source_id": "faq.md#payment",
        "text": "We accept major credit cards, PayPal, and store gift cards. "
        "Payment is charged at the time of shipment, not at the time of "
        "order.",
    },
]

ASSESSMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "scores": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source_id": {"type": "string"},
                    "score": {"type": "number"},
                },
                "required": ["source_id", "score"],
            },
        },
        "covered": {"type": "boolean"},
        "reason": {"type": "string"},
        "answer": {"type": "string"},
        "cited_sources": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["scores", "covered", "reason", "answer", "cited_sources"],
}


_by_id = {doc["source_id"]: doc for doc in FAQ}


def create_assessment_with_retry(**kwargs):
    """Retry one Gemini free-tier rate limit using the delay supplied by the
    API. The normal three-request run fits the quota; this only covers a
    recent earlier demo or another process sharing the same API key."""
    for attempt in range(2):
        try:
            return client.interactions.create(**kwargs)
        except Exception as exc:
            message = str(exc)
            if attempt or "429" not in message and "quota" not in message.lower():
                raise
            retry_after = re.search(r"retry in ([0-9.]+)s", message, re.IGNORECASE)
            wait_seconds = min(60, int(float(retry_after.group(1))) + 1) if retry_after else 60
            print(
                f"Gemini's free-tier request limit is temporarily full; "
                f"retrying this assessment in {wait_seconds} seconds."
            )
            time.sleep(wait_seconds)


def _lookup(source_ids: list[str]) -> list[dict]:
    """Resolves source_ids back to their documents, in the given order.
    Every caller of this passes in an already-ranked list (fused, or
    reranked), and that order is the point: sending a reranker or the
    final answer call a candidate listing in its actual rank order,
    not the FAQ's original declaration order."""
    return [_by_id[source_id] for source_id in source_ids]


def _tokenize(text: str) -> list[str]:
    """Lowercase, whitespace tokenizer. BM25 only needs term overlap, not a
    real NLP pipeline."""
    return text.lower().split()


# Built once, at import time, exactly like a real system would build its
# indexes offline rather than per query.
_bm25_index = BM25Okapi([_tokenize(doc["text"]) for doc in FAQ])


def _embed(texts: list[str]) -> np.ndarray:
    """One embedding call for one or more texts, returned as a matrix (one
    row per text). Used both to build the corpus's vectors once, and to
    embed each incoming query."""
    response = client.models.embed_content(model=EMBEDDING_MODEL, contents=texts)
    return np.array([e.values for e in response.embeddings])


# Also built once: the corpus's own embeddings, computed a single time and
# reused for every query's vector search.
_doc_vectors = _embed([doc["text"] for doc in FAQ])


def bm25_search(query: str, top_k: int = 4) -> list[str]:
    """Keyword search. Returns source_ids ranked by term overlap, best
    first. Strong on exact terms and identifiers, blind to paraphrase."""
    scores = _bm25_index.get_scores(_tokenize(query))
    ranked = sorted(range(len(FAQ)), key=lambda i: scores[i], reverse=True)
    return [FAQ[i]["source_id"] for i in ranked[:top_k]]


def vector_search(query: str, top_k: int = 4) -> list[str]:
    """Dense search. Returns source_ids ranked by cosine similarity between
    the query's embedding and each document's precomputed embedding. Strong
    on paraphrase and meaning, blind to an exact identifier it has never
    seen phrased that way."""
    query_vector = _embed([query])[0]
    similarities = _doc_vectors @ query_vector / (
        np.linalg.norm(_doc_vectors, axis=1) * np.linalg.norm(query_vector)
    )
    ranked = sorted(range(len(FAQ)), key=lambda i: similarities[i], reverse=True)
    return [FAQ[i]["source_id"] for i in ranked[:top_k]]


def reciprocal_rank_fusion(ranked_lists: list[list[str]], k: int = 60) -> list[str]:
    """Merge several ranked lists of source_ids into one, by rank position
    rather than raw score: BM25 and cosine similarity are not on comparable
    scales, but "how far down this list" is something every list shares.
    The exact formula from the lecture's RRF walkthrough."""
    scores: dict[str, float] = {}
    for ranked_list in ranked_lists:
        for position, source_id in enumerate(ranked_list, start=1):
            scores[source_id] = scores.get(source_id, 0.0) + 1.0 / (k + position)
    return sorted(scores, key=lambda source_id: scores[source_id], reverse=True)


def assess_candidates(query: str, candidate_ids: list[str]) -> dict:
    """Use one structured Gemini call to score candidates, judge coverage,
    and draft a cited answer. The pipeline still exposes reranking, coverage,
    and answer as separate stages below, but combines their small-model calls
    so the complete three-question demo fits a five-request free-tier limit.

    A production system may split these decisions for separate tracing and
    evaluation. This compact teaching demo trades that isolation for a
    predictable request budget while retaining each decision's visible output.
    """
    candidates = _lookup(candidate_ids)
    listing = "\n".join(f"{doc['source_id']}: {doc['text']}" for doc in candidates)
    interaction = create_assessment_with_retry(
        model=GENERATION_MODEL,
        input=(
            f"Question: {query}\n\nCandidate passages:\n{listing}\n\n"
            "First score how well each passage answers the question, 0 (not "
            "at all) to 10 (fully answers it). Then decide whether the best "
            "passages actually cover the question rather than merely mention "
            "a related topic. Explain briefly. If covered, draft an answer "
            "using only these passages and cite the source_id values used. If "
            "not covered, return an empty answer and an empty cited_sources list."
        ),
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ASSESSMENT_SCHEMA,
        },
    )
    return json.loads(interaction.output_text)


def refuse(reason: str) -> dict:
    """The clean-failure branch: no answer, a specific reason instead of a
    generic "I don't know." Logging this (a real system would) turns a
    pile of refusals into a signal about what the knowledge base is
    actually missing."""
    return {"answer": None, "refusal_reason": reason}


def show(stage_label: str, payload) -> None:
    print(f"--- {stage_label} ---")
    print(json.dumps(payload, indent=2))
    print()


def run(query: str) -> dict:
    """The whole pipeline, one question at a time, printing its state after
    every stage: hybrid search, fusion, reranking, the coverage check, then
    either a citation or a refusal."""
    print(f"=== {query} ===\n")

    bm25_hits = bm25_search(query)
    show("step 1: BM25 (keyword) hits", bm25_hits)

    vector_hits = vector_search(query)
    show("step 2: vector (dense) hits", vector_hits)

    fused = reciprocal_rank_fusion([bm25_hits, vector_hits])
    show("step 3: fused by reciprocal rank fusion", fused)

    assessment = assess_candidates(query, fused)
    scored = sorted(assessment["scores"], key=lambda score: score["score"], reverse=True)
    reranked = [score["source_id"] for score in scored[:3]]
    show("step 4: reranked, top 3", reranked)

    coverage = {"covered": assessment["covered"], "reason": assessment["reason"]}
    show("step 5: coverage check", coverage)

    if coverage["covered"]:
        result = {
            "answer": assessment["answer"],
            "cited_sources": assessment["cited_sources"],
        }
    else:
        result = refuse(coverage["reason"])
    show("step 6: final result", result)
    return result


if __name__ == "__main__":
    # Three questions, chosen to exercise the pipeline's three interesting
    # paths. See ../module-03/README.md for what each one is meant to show.
    run("What is the warranty period for electronics?")
    run(
        "I bought a blender during a clearance sale and it turned out to be "
        "broken, can I send it back for a refund?"
    )
    run("Do you price-match a lower price found at a competitor's store?")
