from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.compression.context_compression import compress_context
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents

from backend.retrieval.query_understanding.service_detector import detect_service
from backend.retrieval.query_understanding.query_entities import extract_query_entities
from backend.retrieval.query_understanding.schema_detector import is_schema_query

from backend.retrieval.filters.metadata_filter import filter_by_metadata
from backend.retrieval.query_router import get_retrieval_config

from backend.retrieval.core.chunk_store import load_chunks
from backend.retrieval.core.schema_search import schema_search


def retrieve(query):

    service = detect_service(query)

    entities = extract_query_entities(query)

    config = get_retrieval_config(query)

    vector_k = config["vector_k"]
    bm25_k = config["bm25_k"]

    # HYBRID RETRIEVAL (always run)
    candidates = multi_query_retrieval(
        [query],
        service=service,
        vector_k=vector_k,
        bm25_k=bm25_k
    )

    # OPTIONAL SCHEMA AUGMENTATION
    if is_schema_query(query):

        all_chunks = load_chunks()

        schema_candidates = schema_search(query, all_chunks)

        candidates.extend(schema_candidates)

    # METADATA BOOST
    if entities:

        for c in candidates:

            bonus = 0

            if "endpoint" in entities:
                if entities["endpoint"] in c["text"]:
                    bonus += 1.0

            if "http_method" in entities:
                if f"Method: {entities['http_method']}" in c["text"]:
                    bonus += 0.5

            c["metadata_score"] = bonus

        candidates.sort(
            key=lambda x: x.get("metadata_score", 0),
            reverse=True
        )

    # DEDUP
    seen = set()
    unique = []

    for c in candidates:

        cid = c["chunk_id"]

        if cid not in seen:
            seen.add(cid)
            unique.append(c)

    filtered = filter_by_metadata(unique, service)

    reranked = rerank(query, filtered)

    parents = expand_to_parents(reranked)

    compressed = compress_context(query, parents)

    return compressed