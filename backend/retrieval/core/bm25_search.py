import pickle
import json
import numpy as np

BM25_PATH = "data/bm25/bm25.pkl"
CHUNK_PATH = "data/chunks/chunks.json"

with open(BM25_PATH, "rb") as f:
    bm25 = pickle.load(f)

with open(CHUNK_PATH) as f:
    chunks = json.load(f)


def bm25_search(query, k=20):

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    top_indices = np.argsort(scores)[::-1][:k]

    return [chunks[i] for i in top_indices]