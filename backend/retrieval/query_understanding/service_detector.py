def detect_service(query):

    q = query.lower()

    if "stripe" in q:
        return "stripe"

    if "github" in q:
        return "github"

    if "kubernetes" in q or "k8s" in q:
        return "kubernetes"

    return None