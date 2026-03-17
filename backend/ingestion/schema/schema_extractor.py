def build_schema_chunks(spec):

    chunks = []

    components = spec.get("components", {})
    schemas = components.get("schemas", {})

    for name, schema in schemas.items():

        props = schema.get("properties", {})

        lines = [f"Object: {name}", "Fields:"]

        for field, meta in props.items():

            field_type = meta.get("type", "unknown")

            lines.append(f"{field} ({field_type})")

        text = "\n".join(lines)

        chunks.append({
            "document_type": "schema",
            "schema_name": name,
            "text": text
        })

    return chunks