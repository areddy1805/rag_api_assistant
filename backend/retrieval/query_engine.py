import json
import tiktoken

from retrieval.multi_query import multi_query_retrieval
from reranking.reranker import rerank
from llm.generator import generate
from retrieval.context_compression import compress_context

enc = tiktoken.get_encoding("cl100k_base")

PARENT_PATH = "data/chunks/parents.json"


def rewrite_query(query):

    prompt = f"""
Rewrite the following question into a concise search query.

Rules:
Return only the search query.

Question:
{query}
"""

    answer = generate(prompt)

    return answer.strip().replace('"', "")


def generate_queries(query):

    prompt = f"""
Generate 3 search queries with the same meaning.

Return each query on a new line.

Question:
{query}
"""

    result = generate(prompt)

    lines = result.split("\n")

    cleaned = []

    for l in lines:

        l = l.strip()
        l = l.lstrip("0123456789.- ")

        if l:
            cleaned.append(l)

    return cleaned


def load_parents():

    with open(PARENT_PATH) as f:
        parents = json.load(f)

    return {p["parent_id"]: p for p in parents}


def expand_to_parents(children):

    parent_map = load_parents()

    parent_ids = set(c["parent_id"] for c in children)

    return [parent_map[p] for p in parent_ids]


def ask(question):

    rewritten = rewrite_query(question)

    queries = [rewritten] + generate_queries(rewritten)

    candidates = multi_query_retrieval(queries)

    if not candidates:
        return "No relevant documents found."

    retrieved = rerank(rewritten, candidates)

    parents = expand_to_parents(retrieved)

    compressed = compress_context(rewritten, parents, sentences_per_chunk=4)

    context = "\n\n".join([c["text"] for c in compressed])

    max_context_tokens = 3000

    tokens = enc.encode(context)

    if len(tokens) > max_context_tokens:

        tokens = tokens[:max_context_tokens]
        context = enc.decode(tokens)

    prompt = f"""
    Answer the question using the provided documents.

    If the answer is partially present, provide the best answer
    based on the information available.

    Only respond "I don't know" if the documents contain
    no relevant information at all.

    Documents:
    {context}

    Question:
    {question}
    """

    answer = generate(prompt)

    return answer