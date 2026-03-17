import json

PARENT_PATH = "data/processed_docs/parents.json"

with open(PARENT_PATH) as f:
    parents = json.load(f)

parent_map = {p["parent_id"]: p for p in parents}


def expand_to_parents(children):

    parents = []

    seen = set()

    for child in children:

        pid = child["parent_id"]

        if pid in seen:
            continue

        parent = parent_map[pid].copy()

        # propagate metadata from child
        parent["chunk_id"] = child.get("chunk_id")
        parent["parent_id"] = pid
        parent["source"] = child.get("source")
        parent["page"] = child.get("page")

        parents.append(parent)

        seen.add(pid)

    return parents