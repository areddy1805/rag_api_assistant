import sys
import os
import json

# add project root to python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from retrieval.multi_query import multi_query_retrieval
from reranking.reranker import rerank
from retrieval.query_engine import rewrite_query, generate_queries, ask
from llm.generator import generate


DATASET_PATH = "evaluation/dataset.json"


def judge_answer(question, expected, model_answer):

    prompt = f"""
Evaluate the answer produced by a RAG system.

Score from 1 to 5.

5 = fully correct
4 = mostly correct
3 = partially correct
2 = mostly incorrect
1 = incorrect

Return ONLY the number.

Question:
{question}

Expected Answer:
{expected}

Model Answer:
{model_answer}
"""

    result = generate(prompt)

    try:
        score = int(result.strip())
    except:
        score = 0

    return score


def evaluate():

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    total = len(dataset)

    retrieval_hits = 0
    answer_scores = []

    print("\nStarting Evaluation")
    print("=" * 60)

    for item in dataset:

        question = item["question"]
        expected_answer = item["expected_answer"]
        expected_chunk = item["chunk_id"]

        print("\nQuestion:", question)

        # -------------------------
        # Retrieval pipeline
        # -------------------------

        rewritten = rewrite_query(question)

        queries = [rewritten] + generate_queries(rewritten)

        candidates = multi_query_retrieval(queries)

        retrieved = rerank(rewritten, candidates)

        retrieved_chunks = [c["chunk_id"] for c in retrieved]

        print("Expected chunk:", expected_chunk)
        print("Retrieved chunks:", retrieved_chunks)

        if expected_chunk in retrieved_chunks:
            retrieval_hits += 1

        # debug preview
        for c in retrieved:
            print("\nChunk:", c["chunk_id"])
            print(c["text"][:200])

        # -------------------------
        # Generation pipeline
        # -------------------------

        model_answer = ask(question)

        print("\nModel answer:")
        print(model_answer)

        score = judge_answer(question, expected_answer, model_answer)

        print("Answer score:", score)

        answer_scores.append(score)

    recall = retrieval_hits / total
    avg_score = sum(answer_scores) / total if total > 0 else 0

    print("\n")
    print("=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)

    print("Total questions:", total)
    print("Chunk Recall@3:", round(recall, 3))
    print("Average Answer Score:", round(avg_score, 2))


if __name__ == "__main__":
    evaluate()