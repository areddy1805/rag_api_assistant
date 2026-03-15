from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.compression.context_compression import compress_context
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents
from backend.retrieval.query_understanding.service_detector import detect_service
from backend.retrieval.filters.metadata_filter import filter_by_metadata


def retrieve(query):

    service = detect_service(query)

    candidates = multi_query_retrieval([query], service)

    reranked = rerank(query, candidates)

    parents = expand_to_parents(reranked)

    compressed = compress_context(query, parents)

    return compressed