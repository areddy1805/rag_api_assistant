from backend.retrieval.query_classifier import classify_query


def get_retrieval_config(query):

    qtype = classify_query(query)

    config = {
        "vector_k": 8,
        "bm25_k": 8,
        "rerank_k": 7
    }

    if qtype == "endpoint_lookup":

        config["vector_k"] = 5
        config["bm25_k"] = 15

    elif qtype == "schema_question":

        config["vector_k"] = 15
        config["bm25_k"] = 5

    elif qtype == "parameter_question":

        config["vector_k"] = 10
        config["bm25_k"] = 10

    return config