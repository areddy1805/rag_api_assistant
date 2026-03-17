import tiktoken

from backend.llm.query_llm import rewrite_query, generate_query_expansions
from backend.llm.generator import generate_answer

from backend.retrieval.core.multi_query import multi_query_retrieval
from backend.retrieval.ranking.reranker import rerank
from backend.retrieval.parent_expansion.parent_retriever import expand_to_parents
from backend.retrieval.compression.context_compression import compress_context

from backend.observability.trace import RAGTrace
from backend.observability.logger import logger
from backend.observability.grounding import grounding_score


enc = tiktoken.get_encoding("cl100k_base")


MAX_CONTEXT_TOKENS = 500
MAX_CHUNK_TOKENS = 200


def build_token_limited_context(chunks):

    context_parts = []
    used_chunk_ids = []
    total_tokens = 0

    for c in chunks:

        text = c["text"]
        cid = c["chunk_id"]

        tokens = enc.encode(text)

        if len(tokens) > MAX_CHUNK_TOKENS:
            tokens = tokens[:MAX_CHUNK_TOKENS]
            text = enc.decode(tokens)

        token_count = len(tokens)

        if total_tokens + token_count > MAX_CONTEXT_TOKENS:
            break

        context_parts.append(text)
        used_chunk_ids.append(cid)

        total_tokens += token_count

    context = "\n\n".join(context_parts)

    return context, total_tokens, used_chunk_ids


def build_context(question, trace):

    trace.start_stage("rewrite")
    rewritten = rewrite_query(question)
    trace.end_stage("rewrite")

    trace.start_stage("expansion")
    expansions = generate_query_expansions(rewritten)
    trace.end_stage("expansion")

    queries = [rewritten] + expansions

    logger.info(f"[REWRITE] {rewritten}")
    logger.info(f"[EXPANSIONS] {expansions}")

    trace.start_stage("retrieval")
    candidates = multi_query_retrieval(queries)
    trace.end_stage("retrieval")

    trace.log_retrieval(candidates)

    logger.info(f"[METRICS] retrieval_candidates={len(candidates)}")

    trace.start_stage("rerank")
    ranked = rerank(rewritten, candidates)
    trace.end_stage("rerank")

    trace.log_rerank(ranked)

    logger.info(f"[METRICS] rerank_candidates={len(ranked)}")

    trace.start_stage("parent_expansion")
    parents = expand_to_parents(ranked)
    trace.end_stage("parent_expansion")

    trace.start_stage("compression")
    compressed = compress_context(rewritten, parents)
    trace.end_stage("compression")

    trace.start_stage("context_builder")
    context, token_count, chunk_ids = build_token_limited_context(compressed)
    trace.end_stage("context_builder")

    logger.info(f"[CONTEXT_CHUNKS] {chunk_ids}")
    logger.info(f"[CONTEXT TOKENS] {token_count}")
    logger.info(f"[METRICS] context_chunks={len(chunk_ids)}")

    return context


def ask(question):

    trace = RAGTrace(question)

    context = build_context(question, trace)

    trace.start_stage("generation")
    answer = generate_answer(question, context)
    trace.end_stage("generation")

    score = grounding_score(answer, context)

    logger.info(f"[ANSWER] {answer}")
    logger.info(f"[GROUNDING] score={score}")
    if score < 0.35:
        logger.warning("[HALLUCINATION_RISK] answer poorly grounded")

    trace.finish()

    return answer


def ask_stream(question):

    trace = RAGTrace(question)

    context = build_context(question, trace)

    trace.start_stage("generation")

    tokens = []
    answer_parts = []

    for token in generate_answer(question, context, stream=True):

        tokens.append(token)
        answer_parts.append(token)

        yield token

    trace.end_stage("generation")

    answer = "".join(answer_parts)

    score = grounding_score(answer, context)

    logger.info(f"[ANSWER] {answer}")
    logger.info(f"[GROUNDING] score={score}")

    if score < 0.35:
        logger.warning("[HALLUCINATION_RISK] answer poorly grounded")

    trace.finish()