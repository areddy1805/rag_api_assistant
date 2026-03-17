import re
from backend.retrieval.core.chunk_store import load_chunks


_endpoint_index = None


def build_endpoint_index():

    global _endpoint_index

    chunks = load_chunks()

    index = {}

    for c in chunks:

        match = re.search(r"/v1/[a-zA-Z0-9_/{}-]+", c["text"])

        if match:

            ep = match.group(0)

            if ep not in index:
                index[ep] = []

            index[ep].append(c)

    _endpoint_index = index


def get_endpoint_index():

    global _endpoint_index

    if _endpoint_index is None:
        build_endpoint_index()

    return _endpoint_index