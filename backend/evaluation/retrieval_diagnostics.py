import json
import os
import sys
import re
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from backend.retrieval.core.vector_search import vector_search
from backend.retrieval.core.bm25_search import bm25_search
from backend.retrieval.core.chunk_store import load_chunks
from backend.llm.query_llm import rewrite_query

DATASET_PATH = "backend/evaluation/dataset.json"


def tokenize(text):

    return set(re.findall(r"[a-zA-Z0-9_/]+", text.lower()))


def endpoint(text):

    m = re.search(r"/v1/[a-zA-Z0-9_/{}-]+", text)

    if m:
        return m.group(0)

    return None


def analyze():

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    chunks = load_chunks()

    chunk_lookup = {c["chunk_id"]: c for c in chunks}

    failures = []

    for item in dataset[:50]:

        query = item["question"]
        expected = item["chunk_id"]

        rewritten = rewrite_query(query)

        vector_results = vector_search(rewritten, 30)
        bm25_results = bm25_search(rewritten, 30)

        vector_ids = [c["chunk_id"] for c in vector_results]
        bm25_ids = [c["chunk_id"] for c in bm25_results]

        if expected in vector_ids or expected in bm25_ids:
            continue

        expected_chunk = chunk_lookup[expected]

        q_tokens = tokenize(rewritten)
        c_tokens = tokenize(expected_chunk["text"])

        overlap = q_tokens.intersection(c_tokens)

        q_endpoint = endpoint(rewritten)
        c_endpoint = endpoint(expected_chunk["text"])

        failures.append({
            "query": query,
            "expected": expected,
            "endpoint_query": q_endpoint,
            "endpoint_chunk": c_endpoint,
            "token_overlap": len(overlap)
        })

    print("\n==============================")
    print("RETRIEVAL DIAGNOSTICS")
    print("==============================")

    print("Total failures:", len(failures))

    for f in failures[:10]:

        print("\nQuery:", f["query"])
        print("Expected chunk:", f["expected"])
        print("Query endpoint:", f["endpoint_query"])
        print("Chunk endpoint:", f["endpoint_chunk"])
        print("Token overlap:", f["token_overlap"])


if __name__ == "__main__":
    analyze()