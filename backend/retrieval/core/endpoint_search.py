from backend.retrieval.core.endpoint_index import get_endpoint_index


def endpoint_search(endpoints):

    index = get_endpoint_index()

    results = []

    for ep in endpoints:

        if ep in index:

            results.extend(index[ep])

    return results