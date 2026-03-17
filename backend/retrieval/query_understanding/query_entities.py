import re


def extract_query_entities(query: str):

    entities = {}

    # endpoint
    endpoint = re.search(r"/v1/[a-zA-Z0-9_/{}-]+", query)
    if endpoint:
        entities["endpoint"] = endpoint.group(0)

    # http method
    q = query.lower()

    if "post" in q:
        entities["http_method"] = "post"

    elif "get" in q:
        entities["http_method"] = "get"

    elif "delete" in q:
        entities["http_method"] = "delete"

    elif "put" in q:
        entities["http_method"] = "put"

    elif "patch" in q:
        entities["http_method"] = "patch"

    return entities