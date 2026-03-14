import tiktoken
from backend.llm.query_llm import rewrite_query, generate_query_expansions
from backend.llm.generator import generate_answer
from backend.retrieval.query_engine import retrieve

enc = tiktoken.get_encoding("cl100k_base")


def build_context(question):

    rewritten = rewrite_query(question)

    expansions = generate_query_expansions(rewritten)

    queries = [rewritten] + expansions

    context_chunks = retrieve(queries)

    context = "\n\n".join([c["text"] for c in context_chunks])

    max_context_tokens = 1200

    tokens = enc.encode(context)

    if len(tokens) > max_context_tokens:
        tokens = tokens[:max_context_tokens]
        context = enc.decode(tokens)

    return context


def ask(question):

    context = build_context(question)

    return generate_answer(question, context)


def ask_stream(question):

    context = build_context(question)

    for token in generate_answer(question, context, stream=True):
        yield token