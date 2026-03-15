import pickle
import json
import numpy as np
import re

BM25_PATH = "data/bm25/bm25.pkl"
CHUNK_PATH = "data/processed_docs/chunks.json"

with open(BM25_PATH, "rb") as f:
    bm25 = pickle.load(f)

with open(CHUNK_PATH) as f:
    chunks = json.load(f)


def bm25_search(query, k=20, service=None):

    tokenized_query = re.findall(r"[a-zA-Z0-9_/]+", query.lower())

    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:k]

    results = [chunks[i] for i in top_indices]

    if service:
        results = [r for r in results if r.get("service_name") == service]

    return results