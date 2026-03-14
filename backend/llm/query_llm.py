from backend.llm.client import chat


def rewrite_query(query):

    prompt = f"""
Rewrite the following question into a concise search query.

Return only the search query.

Question:
{query}
"""

    return chat(prompt).strip()


def generate_query_expansions(query):

    prompt = f"""
Generate 3 search queries with the same meaning.

Return each query on a new line.

Question:
{query}
"""

    result = chat(prompt)

    lines = result.split("\n")

    cleaned = []

    for l in lines:
        l = l.strip()
        l = l.lstrip("0123456789.- ")

        if l:
            cleaned.append(l)

    return cleaned