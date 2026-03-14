import sys
import os
import json
import time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from backend.services.chat_service import ask
from backend.llm.client import chat, ANSWER_MODEL

DATASET_PATH = "backend/evaluation/dataset.json"

MAX_EVAL = 50
SLEEP_TIME = 2


def judge_answer(question, expected, model_answer):

    prompt = f"""
Evaluate the model answer.

Score from 1 to 5.

5 = correct
4 = mostly correct
3 = partially correct
2 = weak
1 = incorrect

Return ONLY the number.

Question:
{question}

Expected Answer:
{expected}

Model Answer:
{model_answer}
"""

    result = chat(prompt,ANSWER_MODEL)

    try:
        score = int(result.strip())
    except:
        score = 0

    return score


def evaluate():

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    dataset = dataset[:MAX_EVAL]

    total = len(dataset)
    scores = []

    print("\nStarting Generation Evaluation")
    print("="*60)

    for item in dataset:

        question = item["question"]
        expected = item["expected_answer"]

        print("\nQuestion:", question)

        answer = ask(question)

        print("\nModel Answer:")
        print(answer)

        score = judge_answer(question, expected, answer)

        print("Score:", score)

        scores.append(score)

        time.sleep(SLEEP_TIME)

    avg = sum(scores) / total

    print("\n")
    print("="*60)
    print("GENERATION RESULTS")
    print("="*60)

    print("Total questions:", total)
    print("Average Score:", round(avg,2))


if __name__ == "__main__":
    evaluate()