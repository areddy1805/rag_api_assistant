import json

CHUNK_PATH = "data/processed_docs/chunks.json"

_chunks = None


def load_chunks():

    global _chunks

    if _chunks is None:

        with open(CHUNK_PATH) as f:
            _chunks = json.load(f)

    return _chunks