def metadata_search(chunks, entities):

    if not entities:
        return []

    results = []

    for chunk in chunks:

        match = True

        if "endpoint" in entities:
            if chunk.get("endpoint") != entities["endpoint"]:
                match = False

        if "http_method" in entities:
            if chunk.get("http_method") != entities["http_method"]:
                match = False

        if match:
            results.append(chunk)

    return results