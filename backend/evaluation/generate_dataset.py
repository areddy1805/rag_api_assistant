import sys
import os
import json
import random
import time
import re

from backend.llm.client import chat, REWRITE_MODEL

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

CHUNKS_PATH = "data/processed_docs/chunks.json"
OUTPUT_PATH = "backend/evaluation/dataset.json"

NUM_SAMPLES = 100
SLEEP_TIME = 1.5


def load_chunks():
    with open(CHUNKS_PATH) as f:
        return json.load(f)


def generate_question(chunk):

    prompt = f"""
You are generating evaluation questions for a developer API retrieval system.

Create ONE question whose answer can ONLY be found in the passage below.

STRICT RULES

1. The question MUST contain a specific identifier from the text such as:
   - API endpoint path (example: /v1/payment_intents)
   - parameter name
   - object name
   - field name

2. The question MUST NOT be generic.

Bad examples:
- What HTTP method is used for this endpoint?
- What is the description of this API operation?

Good examples:
- What HTTP method is used for the endpoint /v1/payment_intents?
- What endpoint path creates a PaymentIntent in the Stripe API?

3. The answer MUST appear verbatim in the passage.

Return JSON only in the format:

{{
  "question": "...",
  "answer": "..."
}}

Passage:
{chunk["text"]}
"""

    result = chat(prompt, REWRITE_MODEL)

    try:
        return json.loads(result)
    except:
        return None


def extract_identifiers(text):

    endpoints = re.findall(r"/v1/[a-zA-Z0-9_/{{}}-]+", text)

    fields = re.findall(r"[a-zA-Z_]{4,}", text)

    return set(endpoints + fields)


def build_dataset():

    chunks = load_chunks()

    dataset = []

    api_chunks = [c for c in chunks if "/v1/" in c["text"]]

    if len(api_chunks) > NUM_SAMPLES:
        sampled_chunks = random.sample(api_chunks, NUM_SAMPLES)
    else:
        sampled_chunks = random.sample(chunks, min(NUM_SAMPLES, len(chunks)))

    for chunk in sampled_chunks:

        print("\nGenerating QA for chunk:", chunk["chunk_id"])

        qa = generate_question(chunk)

        if not qa:
            print("Failed parsing JSON. Skipping.")
            continue

        if "question" not in qa or "answer" not in qa:
            print("Malformed QA. Skipping.")
            continue

        answer = qa["answer"].strip().lower()

        if len(answer) < 2:
            print("Answer too short. Skipping.")
            continue

        valid_methods = ["get", "post", "delete", "put", "patch"]

        if answer not in valid_methods:
            bad_answers = ["yes", "no", "true", "false"]
            if answer in bad_answers:
                print("Generic answer. Skipping.")
                continue

        identifiers = extract_identifiers(chunk["text"])

        question_lower = qa["question"].lower()

        if not any(identifier.lower() in question_lower for identifier in identifiers):
            print("Question lacks identifiers. Skipping.")
            continue

        dataset.append({
            "question": qa["question"],
            "expected_answer": qa["answer"],
            "chunk_id": chunk["chunk_id"],
            "source_page": chunk.get("page")
        })

        print("Q:", qa["question"])
        print("A:", qa["answer"])

        time.sleep(SLEEP_TIME)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(dataset, f, indent=2)

    print("\nDataset saved:", OUTPUT_PATH)
    print("Total questions:", len(dataset))


if __name__ == "__main__":
    build_dataset()