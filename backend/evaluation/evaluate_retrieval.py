import sys
import os
import json
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.llm.query_llm import rewrite_query


DATASET_PATH = "backend/evaluation/dataset.json"
CHUNKS_PATH = "data/processed_docs/chunks.json"

MAX_EVAL = 50
SLEEP_TIME = 1.5


def load_chunk_parent_map():

    with open(CHUNKS_PATH) as f:
        chunks = json.load(f)

    return {c["chunk_id"]: c["parent_id"] for c in chunks}


def evaluate():

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    dataset = dataset[:MAX_EVAL]

    chunk_parent = load_chunk_parent_map()

    total = len(dataset)

    chunk_hits = 0
    parent_hits = 0

    results = []

    print("\nStarting Retrieval Evaluation")
    print("=" * 60)

    for item in dataset:

        question = item["question"]
        expected_chunk = item["chunk_id"]
        expected_parent = chunk_parent.get(expected_chunk)

        print("\nQuestion:", question)

        rewritten = rewrite_query(question)

        candidates = multi_query_retrieval([rewritten])

        retrieved = rerank(rewritten, candidates)

        retrieved_chunks = [c["chunk_id"] for c in retrieved]

        retrieved_parents = [
            chunk_parent.get(cid) for cid in retrieved_chunks
        ]

        print("Expected chunk:", expected_chunk)
        print("Expected parent:", expected_parent)
        print("Retrieved chunks:", retrieved_chunks)
        print("Retrieved parents:", retrieved_parents)

        chunk_hit = expected_chunk in retrieved_chunks
        parent_hit = expected_parent in retrieved_parents

        if chunk_hit:
            chunk_hits += 1

        if parent_hit:
            parent_hits += 1

        results.append({
            "question": question,
            "expected_chunk": expected_chunk,
            "expected_parent": expected_parent,
            "retrieved_chunks": retrieved_chunks,
            "retrieved_parents": retrieved_parents,
            "chunk_hit": chunk_hit,
            "parent_hit": parent_hit
        })

        time.sleep(SLEEP_TIME)

    chunk_recall = chunk_hits / total
    parent_recall = parent_hits / total

    print("\n")
    print("=" * 60)
    print("RETRIEVAL RESULTS")
    print("=" * 60)

    print("Total questions:", total)
    print("Chunk Recall@3:", round(chunk_recall, 3))
    print("Parent Recall@3:", round(parent_recall, 3))

    return [
        {
            "recall": chunk_recall,
            "parent_recall": parent_recall
        }
    ]