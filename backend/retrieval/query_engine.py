from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.compression.context_compression import compress_context
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents
from backend.retrieval.core.hybrid_search import hybrid_search




def retrieve(query):

    candidates = hybrid_search(query, 20)

    reranked = rerank(query, candidates)

    parents = expand_to_parents(reranked)

    compressed = compress_context(query, parents)

    return compressed