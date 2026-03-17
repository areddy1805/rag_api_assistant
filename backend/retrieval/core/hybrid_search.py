import re
from backend.retrieval.core.vector_search import vector_search
from backend.retrieval.core.bm25_search import bm25_search
from backend.retrieval.query_understanding.endpoint_extractor import extract_endpoints


def hybrid_search(query, vector_k=8, bm25_k=8, final_k=10, service=None):

    vector_results = vector_search(query, vector_k)
    bm25_results = bm25_search(query, bm25_k)

    if service:

        vector_results = [
            r for r in vector_results
            if r.get("service_name") == service
        ]

        bm25_results = [
            r for r in bm25_results
            if r.get("service_name") == service
        ]

    scores = {}
    k_rrf = 60

    # RRF FUSION

    for rank, r in enumerate(vector_results):

        cid = r["chunk_id"]

        score = 1 / (k_rrf + rank)

        scores[cid] = scores.get(cid, 0) + score

    for rank, r in enumerate(bm25_results):

        cid = r["chunk_id"]

        score = 1 / (k_rrf + rank)

        scores[cid] = scores.get(cid, 0) + score

    lookup = {}

    for r in vector_results + bm25_results:
        lookup[r["chunk_id"]] = r

    # ENDPOINT BOOST (POST-FUSION)

    endpoints = extract_endpoints(query)
    endpoint_bonus = 0.75

    if endpoints:

        for cid in scores:

            chunk = lookup.get(cid)

            if not chunk:
                continue

            match = re.search(r"Endpoint:\s*(/v1/[^\s]+)", chunk["text"])

            if match:

                chunk_ep = match.group(1)

                if chunk_ep in endpoints:
                    scores[cid] += endpoint_bonus

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    results = []

    for cid, _ in ranked[:final_k]:

        if cid in lookup:
            results.append(lookup[cid])

    return results