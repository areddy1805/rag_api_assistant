import json

INPUT_PATH = "data/chunks/chunks.json"
OUTPUT_PATH = "data/chunks/parents.json"

PARENT_SIZE = 1000


def build_parents():

    with open(INPUT_PATH) as f:
        chunks = json.load(f)

    parents = []
    parent_id = 0
    current = []

    token_count = 0

    for c in chunks:

        tokens = c["text"].split()
        length = len(tokens)

        if token_count + length > PARENT_SIZE:

            parents.append({
                "parent_id": parent_id,
                "text": " ".join(current)
            })

            parent_id += 1
            current = []
            token_count = 0

        current.append(c["text"])
        token_count += length

    if current:

        parents.append({
            "parent_id": parent_id,
            "text": " ".join(current)
        })

    with open(OUTPUT_PATH,"w") as f:
        json.dump(parents,f,indent=2)


if __name__ == "__main__":
    build_parents()