import sys
import os
import orjson

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from backend.ingestion.pipeline import ingest_document

RAW_DOCS = "data/raw_docs"

CHUNK_PATH = "data/processed_docs/chunks.json"
PARENT_PATH = "data/processed_docs/parents.json"

all_parents = []
all_children = []

for root, _, files in os.walk(RAW_DOCS):

    for f in files:

        path = os.path.join(root, f)

        print("Ingesting:", path)

        try:

            parents, children = ingest_document(path)

            all_parents.extend(parents)
            all_children.extend(children)

        except Exception as e:

            print("Failed:", path)
            print(e)

os.makedirs("data/processed_docs", exist_ok=True)

with open(CHUNK_PATH, "wb") as f:
    f.write(orjson.dumps(all_children))

with open(PARENT_PATH, "wb") as f:
    f.write(orjson.dumps(all_parents))

print("Parents:", len(all_parents))
print("Children:", len(all_children))