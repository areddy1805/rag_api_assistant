from backend.retrieval.core.hybrid_search import hybrid_search


def multi_query_retrieval(queries, service=None, vector_k=8, bm25_k=8):

    all_chunks = {}

    for q in queries:

        results = hybrid_search(q, vector_k=vector_k, bm25_k=bm25_k)

        for r in results:
            all_chunks[r["chunk_id"]] = r

    return list(all_chunks.values())