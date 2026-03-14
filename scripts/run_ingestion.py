import os
import orjson

from ingest import load_doc, build_parent_child_chunks


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DOC_PATH = os.path.join(PROJECT_ROOT, "../data/eBook-How-to-Build-a-Career-in-AI.pdf")

CHUNK_PATH = os.path.join(PROJECT_ROOT, "data/chunks/chunks.json")
PARENT_PATH = os.path.join(PROJECT_ROOT, "data/chunks/parents.json")


# load document
pages = load_doc(DOC_PATH)

# build parent + child chunks
parents, children = build_parent_child_chunks(pages)


# ensure directory exists
os.makedirs(os.path.dirname(CHUNK_PATH), exist_ok=True)


# save children
with open(CHUNK_PATH, "wb") as f:
    f.write(orjson.dumps(children))


# save parents
with open(PARENT_PATH, "wb") as f:
    f.write(orjson.dumps(parents))


print("Parents saved:", len(parents))
print("Child chunks saved:", len(children))