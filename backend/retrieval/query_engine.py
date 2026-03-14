from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.compression.context_compression import compress_context
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents


def retrieve(queries):

    candidates = multi_query_retrieval(queries)

    reranked = rerank(queries[0], candidates)

    parents = expand_to_parents(reranked)

    compressed = compress_context(queries[0], parents)

    return compressed