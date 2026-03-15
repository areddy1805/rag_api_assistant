from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.compression.context_compression import compress_context
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents
from backend.retrieval.query_understanding.service_detector import detect_service
from backend.retrieval.filters.metadata_filter import filter_by_metadata
from backend.retrieval.query_router import get_retrieval_config


def retrieve(query):

    # detect service (stripe, github, kubernetes, etc.)
    service = detect_service(query)

    # determine retrieval strategy
    config = get_retrieval_config(query)

    vector_k = config["vector_k"]
    bm25_k = config["bm25_k"]

    # multi-query retrieval using routed parameters
    candidates = multi_query_retrieval(
        [query],
        service=service,
        vector_k=vector_k,
        bm25_k=bm25_k
    )

    # metadata filtering (service-specific docs)
    filtered = filter_by_metadata(candidates, service)

    # rerank candidates
    reranked = rerank(query, filtered)

    # expand children → parent sections
    parents = expand_to_parents(reranked)

    # sentence-level compression
    compressed = compress_context(query, parents)

    return compressed