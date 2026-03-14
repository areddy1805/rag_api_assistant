from backend.llm.query_llm import rewrite_query
from backend.llm.query_llm import generate_query_expansions
from backend.llm.generator import generate_answer
from backend.retrieval.query_engine import retrieve


def ask(question):

    rewritten = rewrite_query(question)

    expansions = generate_query_expansions(rewritten)

    queries = [rewritten] + expansions

    context_chunks = []

    for q in queries:
        results = retrieve(q)
        context_chunks.extend(results)

    context = "\n\n".join([c["text"] for c in context_chunks])

    answer = generate_answer(question, context)

    return answer