from backend.llm.client import chat


def generate_answer(question, context):

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

    return chat(prompt)