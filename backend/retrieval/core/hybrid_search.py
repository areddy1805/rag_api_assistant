from retrieval.vector_search import vector_search
from retrieval.bm25_search import bm25_search


def hybrid_search(query, k=10):

    vector_results = vector_search(query, 10)
    bm25_results = bm25_search(query, 10)

    scores = {}
    k_rrf = 60

    for rank, r in enumerate(vector_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0) + 1/(k_rrf + rank)

    for rank, r in enumerate(bm25_results):
        cid = r["chunk_id"]
        scores[cid] = scores.get(cid, 0) + 1/(k_rrf + rank)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    results = []

    for cid, _ in ranked[:k]:
        results.append(vector_results[0] if False else next(
            c for c in vector_results + bm25_results if c["chunk_id"] == cid
        ))

    return results