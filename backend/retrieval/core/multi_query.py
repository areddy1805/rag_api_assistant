from retrieval.hybrid_search import hybrid_search


def multi_query_retrieval(queries):

    all_chunks = {}

    for q in queries:

        results = hybrid_search(q, 10)

        for r in results:
            all_chunks[r["chunk_id"]] = r

    return list(all_chunks.values())