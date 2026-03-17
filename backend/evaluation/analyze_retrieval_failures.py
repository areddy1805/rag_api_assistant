import json
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.llm.query_llm import rewrite_query

DATASET_PATH = "backend/evaluation/dataset.json"

VECTOR_K = 30
BM25_K = 30


def analyze():

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    retriever_failures = []
    reranker_failures = []
    successes = []

    for item in dataset:

        query = item["question"]
        expected = item["chunk_id"]

        rewritten = rewrite_query(query)

        candidates = multi_query_retrieval(
            [rewritten],
            vector_k=VECTOR_K,
            bm25_k=BM25_K
        )

        retrieved_ids = [c["chunk_id"] for c in candidates]

        if expected not in retrieved_ids:

            retriever_failures.append({
                "query": query,
                "expected": expected,
                "retrieved": retrieved_ids[:10]
            })

            continue

        reranked = rerank(rewritten, candidates)

        top3 = [c["chunk_id"] for c in reranked[:3]]

        if expected not in top3:

            reranker_failures.append({
                "query": query,
                "expected": expected,
                "reranked": top3
            })

        else:

            successes.append(query)

    print("\n====================================")
    print("RETRIEVAL FAILURE ANALYSIS")
    print("====================================")

    print("Total queries:", len(dataset))
    print("Success:", len(successes))
    print("Retriever failures:", len(retriever_failures))
    print("Reranker failures:", len(reranker_failures))

    print("\n--- Retriever Failures ---")

    for f in retriever_failures[:10]:

        print("\nQuery:", f["query"])
        print("Expected:", f["expected"])
        print("Retrieved:", f["retrieved"])

    print("\n--- Reranker Failures ---")

    for f in reranker_failures[:10]:

        print("\nQuery:", f["query"])
        print("Expected:", f["expected"])
        print("Top3:", f["reranked"])


if __name__ == "__main__":
    analyze()