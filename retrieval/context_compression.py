from sentence_transformers import CrossEncoder
import nltk

model = CrossEncoder("BAAI/bge-reranker-base", device="mps")


def compress_context(query, chunks, sentences_per_chunk=6):

    compressed_chunks = []

    for chunk in chunks:

        sentences = nltk.sent_tokenize(chunk["text"])

        pairs = [[query, s] for s in sentences]

        scores = model.predict(pairs)

        ranked = sorted(
            zip(sentences, scores),
            key=lambda x: x[1],
            reverse=True
        )

        top_sentences = [s for s, _ in ranked[:sentences_per_chunk]]

        compressed_chunks.append({
            "text": " ".join(top_sentences),
            "page": chunk.get("page"),
            "parent_id": chunk.get("parent_id"),
            "chunk_id": chunk.get("chunk_id")
        })

    return compressed_chunks