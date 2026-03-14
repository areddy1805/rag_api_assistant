import json

PARENT_PATH = "data/processed_docs/parents.json"

with open(PARENT_PATH) as f:
    parents = json.load(f)

parent_map = {p["parent_id"]: p for p in parents}


def expand_to_parents(children):

    parent_ids = set(c["parent_id"] for c in children)

    return [parent_map[p] for p in parent_ids]