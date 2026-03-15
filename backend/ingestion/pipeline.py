from dataclasses import asdict

from backend.ingestion.loaders.loader_router import get_loader
from backend.ingestion.ingest import build_parent_child_chunks


def ingest_document(path):

    loader = get_loader(path)

    docs = loader.load(path)

    parents = []
    children = []

    parent_id = 0
    chunk_id = 0

    pages = []

    for d in docs:

        obj = asdict(d)

        service = obj.get("service_name")
        endpoint = obj.get("endpoint")
        method = obj.get("http_method")
        dtype = obj.get("document_type")

        # OPENAPI endpoints → keep as single chunk
        if dtype == "openapi":

            parents.append({
                "parent_id": parent_id,
                "text": obj["text"],
                "page": None,
                "source": obj["source"],
                "service_name": service,
                "endpoint": endpoint,
                "http_method": method,
                "document_type": dtype
            })

            children.append({
                "chunk_id": chunk_id,
                "parent_id": parent_id,
                "text": obj["text"],
                "page": None,
                "source": obj["source"],
                "service_name": service,
                "endpoint": endpoint,
                "http_method": method,
                "document_type": dtype
            })

            parent_id += 1
            chunk_id += 1

        else:

            pages.append({
                "text": obj.get("text", ""),
                "page": obj.get("page", 0),
                "source": obj.get("source", path),
                "service_name": service,
                "document_type": dtype
            })

    # run chunker only on non-openapi docs
    if pages:

        p, c = build_parent_child_chunks(pages)

        for parent in p:

            parent["service_name"] = pages[0].get("service_name")
            parent["document_type"] = pages[0].get("document_type")

        for child in c:

            child["service_name"] = pages[0].get("service_name")
            child["document_type"] = pages[0].get("document_type")

        parents.extend(p)
        children.extend(c)

    return parents, children