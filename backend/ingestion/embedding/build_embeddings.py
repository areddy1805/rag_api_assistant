import json
import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi

CHILD_PATH = "data/chunks/chunks.json"
PARENT_PATH = "data/chunks/parents.json"

EMBED_PATH = "data/embeddings/embeddings.npy"
INDEX_PATH = "data/index/faiss.index"
BM25_PATH = "data/bm25/bm25.pkl"

model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="mps")


with open(CHILD_PATH) as f:
    children = json.load(f)

texts = [c["text"] for c in children]

print("Total child chunks:", len(texts))


embeddings = model.encode(
    texts,
    normalize_embeddings=True
)

print("Embedding shape:", embeddings.shape)


os.makedirs("data/embeddings", exist_ok=True)
np.save(EMBED_PATH, embeddings)

print("Embeddings saved")


dim = embeddings.shape[1]

index = faiss.IndexFlatIP(dim)
index.add(embeddings.astype("float32"))

os.makedirs("data/index", exist_ok=True)
faiss.write_index(index, INDEX_PATH)

print("FAISS index saved")


tokenized = [t.lower().split() for t in texts]

bm25 = BM25Okapi(tokenized)

os.makedirs("data/bm25", exist_ok=True)

with open(BM25_PATH, "wb") as f:
    pickle.dump(bm25, f)

print("BM25 index saved")