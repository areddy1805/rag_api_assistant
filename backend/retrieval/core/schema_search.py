def schema_search(query, chunks):

    q = query.lower()

    results = []

    for c in chunks:

        if c.get("document_type") != "schema":
            continue

        if c.get("schema_name", "").lower() in q:
            results.append(c)

    return results