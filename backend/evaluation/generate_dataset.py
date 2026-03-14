import sys
import os
import json
import random
import time
from backend.llm.client import chat

# add project root to python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)


CHUNKS_PATH = "data/processed_docs/chunks.json"
OUTPUT_PATH = "backend/evaluation/dataset.json"

# number of questions to generate
NUM_SAMPLES = 100
SLEEP_TIME = 1.5

def load_chunks():

    with open(CHUNKS_PATH) as f:
        chunks = json.load(f)

    return chunks


def generate_question(chunk):

    prompt = f"""
You are creating evaluation questions for a retrieval system.

From the following passage generate ONE factual question
that can be answered ONLY using this passage.

Return JSON in the format:

{{
 "question": "...",
 "answer": "..."
}}

Rules:
- Question must be clear and factual
- Answer must be short (1–2 sentences)
- Do not include explanation
- Output only JSON

Passage:
{chunk["text"]}
"""

    result = chat(prompt)

    try:
        data = json.loads(result)
    except:
        return None

    return data


def build_dataset():

    chunks = load_chunks()

    dataset = []

    sampled_chunks = random.sample(chunks, min(NUM_SAMPLES, len(chunks)))

    for chunk in sampled_chunks:

        print("\nGenerating QA for chunk:", chunk["chunk_id"])

        qa = generate_question(chunk)

        if not qa:
            print("Failed parsing JSON. Skipping.")
            continue

        dataset.append({
            "question": qa["question"],
            "expected_answer": qa["answer"],
            "chunk_id": chunk["chunk_id"],
            "source_page": chunk["page"]
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