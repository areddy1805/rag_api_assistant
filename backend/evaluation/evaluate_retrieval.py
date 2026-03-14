import sys
import os
import json
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from retrieval.multi_query import multi_query_retrieval
from reranking.reranker import rerank
from retrieval.query_engine import rewrite_query

DATASET_PATH = "evaluation/dataset.json"

MAX_EVAL = 50
SLEEP_TIME = 1.5


def evaluate():

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    dataset = dataset[:MAX_EVAL]

    total = len(dataset)
    retrieval_hits = 0

    print("\nStarting Retrieval Evaluation")
    print("="*60)

    for item in dataset:

        question = item["question"]
        expected_chunk = item["chunk_id"]

        print("\nQuestion:", question)

        rewritten = rewrite_query(question)

        candidates = multi_query_retrieval([rewritten])

        retrieved = rerank(rewritten, candidates)

        retrieved_chunks = [c["chunk_id"] for c in retrieved]

        print("Expected chunk:", expected_chunk)
        print("Retrieved chunks:", retrieved_chunks)

        if expected_chunk in retrieved_chunks:
            retrieval_hits += 1

        time.sleep(SLEEP_TIME)

    recall = retrieval_hits / total

    print("\n")
    print("="*60)
    print("RETRIEVAL RESULTS")
    print("="*60)

    print("Total questions:", total)
    print("Chunk Recall@3:", round(recall, 3))


if __name__ == "__main__":
    evaluate()