from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

cache_vectors = []
cache_answers = []

SIM_THRESHOLD = 0.92

def check_cache(query):

    if not cache_vectors:
        return None

    qvec = model.encode([query])[0]

    sims = np.dot(cache_vectors, qvec)

    idx = sims.argmax()

    if sims[idx] > SIM_THRESHOLD:
        return cache_answers[idx]

    return None


def store_cache(query, answer):

    vec = model.encode([query])[0]

    cache_vectors.append(vec)
    cache_answers.append(answer)