import re


def tokenize(text):

    return set(
        re.findall(r"[a-zA-Z0-9_/]+", text.lower())
    )


def grounding_score(answer, context):

    answer_tokens = tokenize(answer)

    context_tokens = tokenize(context)

    if not answer_tokens:
        return 0.0

    overlap = answer_tokens.intersection(context_tokens)

    score = len(overlap) / len(answer_tokens)

    return round(score, 3)