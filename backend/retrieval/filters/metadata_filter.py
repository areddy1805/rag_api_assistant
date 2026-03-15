def filter_by_metadata(chunks, service=None):

    if not service:
        return chunks

    filtered = []

    for c in chunks:

        if c.get("service_name") == service:
            filtered.append(c)

    return filtered