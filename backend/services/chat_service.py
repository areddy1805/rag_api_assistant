import tiktoken

from backend.llm.query_llm import rewrite_query, generate_query_expansions
from backend.llm.generator import generate_answer
from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents
from backend.retrieval.compression.context_compression import compress_context

enc = tiktoken.get_encoding("cl100k_base")


def build_context(question):

    rewritten = rewrite_query(question)

    expansions = generate_query_expansions(rewritten)

    queries = [rewritten] + expansions

    # retrieve candidates for all queries
    candidates = multi_query_retrieval(queries)

    # rerank using rewritten query
    ranked = rerank(rewritten, candidates)

    # parent expansion
    parents = expand_to_parents(ranked)

    # compression
    compressed = compress_context(rewritten, parents)

    context = "\n\n".join([c["text"] for c in compressed])

    max_tokens = 1200

    tokens = enc.encode(context)

    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        context = enc.decode(tokens)

    return context


def ask(question):

    context = build_context(question)

    return generate_answer(question, context)


def ask_stream(question):

    context = build_context(question)

    for token in generate_answer(question, context, stream=True):
        yield token