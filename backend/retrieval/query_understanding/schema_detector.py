def is_schema_query(query):

    q = query.lower()

    schema_keywords = [
        "field",
        "parameter",
        "schema",
        "request body",
        "payload",
        "properties",
        "required"
    ]

    return any(k in q for k in schema_keywords)