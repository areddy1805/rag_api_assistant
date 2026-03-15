from dataclasses import asdict

from backend.ingestion.loaders.loader_router import get_loader
from backend.ingestion.ingest import build_parent_child_chunks


def ingest_document(path):

    loader = get_loader(path)

    docs = loader.load(path)

    pages = []

    for d in docs:

        if isinstance(d, dict):
            pages.append(d)

        else:
            obj = asdict(d)

            pages.append({
                "text": obj.get("text", ""),
                "page": obj.get("page", 0),
                "source": obj.get("source", path)
            })

    parents, children = build_parent_child_chunks(pages)

    return parents, children