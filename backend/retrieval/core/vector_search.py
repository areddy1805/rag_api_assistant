import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import json
import torch

INDEX_PATH = "index/faiss.index"
CHUNK_PATH = "data/processed_docs/chunks.json"

index = faiss.read_index(INDEX_PATH)

with open(CHUNK_PATH) as f:
    chunks = json.load(f)

model = SentenceTransformer("BAAI/bge-small-en-v1.5",device = "mps" if torch.backends.mps.is_available() else "cpu")


def vector_search(query, k=20):

    query = "Represent this sentence for searching relevant passages: " + query

    q_emb = model.encode([query], normalize_embeddings=True)

    scores, indices = index.search(np.array(q_emb).astype("float32"), k)

    return [chunks[i] for i in indices[0]]