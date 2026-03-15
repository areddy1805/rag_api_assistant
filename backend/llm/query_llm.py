from backend.llm.client import chat, REWRITE_MODEL


def rewrite_query(query):

    prompt = f"""
Rewrite the question into a concise search query.

Rules:
- Preserve API names exactly.
- Preserve endpoint paths like /v1/payment_intents.
- Preserve technical terms such as Stripe, GitHub, Kubernetes.
- Do NOT paraphrase endpoint paths.
- Output only the rewritten query.

Question:
{query}
"""

    return chat(prompt, REWRITE_MODEL).strip()


def generate_query_expansions(query):

    prompt = f"""
Generate 2 alternative search queries.

Rules:
- Preserve API endpoint paths exactly.
- Preserve API names such as Stripe, GitHub, Kubernetes.
- Do NOT remove technical tokens.
- Each query should be slightly different wording.

Return each query on a new line.

Query:
{query}
"""

    result = chat(prompt, REWRITE_MODEL)

    lines = result.split("\n")

    cleaned = []

    for l in lines:

        l = l.strip()
        l = l.lstrip("0123456789.- ")

        if l:
            cleaned.append(l)

    return cleaned