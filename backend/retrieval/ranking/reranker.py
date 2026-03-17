from sentence_transformers import CrossEncoder
import torch

model = CrossEncoder("BAAI/bge-reranker-base",device = "mps" if torch.backends.mps.is_available() else "cpu")

def rerank(query, chunks, top_k=7):

    pairs = [[query,c["text"]] for c in chunks]

    scores = model.predict(pairs, batch_size=16)

    ranked = sorted(
        zip(chunks,scores),
        key=lambda x:x[1],
        reverse=True
    )

    return [c for c,_ in ranked[:top_k]]