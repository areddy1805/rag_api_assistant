import re


def classify_query(query: str) -> str:

    q = query.lower()

    if re.search(r"/v1/", q):
        return "endpoint_lookup"

    if "endpoint" in q:
        return "endpoint_lookup"

    if "http method" in q:
        return "endpoint_lookup"

    if "parameter" in q:
        return "parameter_question"

    if "field" in q or "schema" in q:
        return "schema_question"

    if "example" in q:
        return "example_request"

    if "error" in q:
        return "error_explanation"

    return "general_docs"