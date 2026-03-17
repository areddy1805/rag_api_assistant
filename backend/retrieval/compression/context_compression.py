from sentence_transformers import CrossEncoder
import nltk
import torch

model = CrossEncoder(
    "BAAI/bge-reranker-base",
    device="mps" if torch.backends.mps.is_available() else "cpu"
)


def compress_context(query, chunks, sentences_per_chunk=4):

    compressed_chunks = []

    for chunk in chunks:

        text = chunk.get("text", "")

        sentences = nltk.sent_tokenize(text)

        if not sentences:
            continue

        pairs = [[query, s] for s in sentences]

        scores = model.predict(pairs)

        ranked = sorted(
            enumerate(zip(sentences, scores)),
            key=lambda x: x[1][1],
            reverse=True
        )

        top = ranked[:sentences_per_chunk]

        top_sorted = sorted(top, key=lambda x: x[0])

        top_sentences = [s for _, (s, _) in top_sorted]

        compressed_chunks.append({
            "text": " ".join(top_sentences),

            # metadata propagated safely
            "chunk_id": chunk.get("chunk_id"),
            "parent_id": chunk.get("parent_id"),
            "page": chunk.get("page"),
            "source": chunk.get("source")
        })

    return compressed_chunks