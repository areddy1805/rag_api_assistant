System architecture specification.

⸻

System Type

Retrieval Augmented Generation (RAG)
Hybrid Retrieval + Parent-Child Context Expansion + Sentence Compression

Purpose:

Answer questions using document knowledge with high retrieval accuracy
and controlled context grounding.

⸻

High-Level Pipeline

Documents
↓
Ingestion
↓
Parent-Child Chunking
↓
Embedding + Indexing
↓
Hybrid Retrieval
↓
Reranking
↓
Parent Expansion
↓
Sentence-Level Context Compression
↓
Prompt Construction
↓
LLM Generation
↓
Answer

⸻

Repository Architecture

rag_v1/
│
├── ingestion/
│ ├── semantic_chunk.py
│ ├── build_embeddings.py
│ └── run_ingestion.py
│
├── retrieval/
│ ├── vector_search.py
│ ├── bm25_search.py
│ ├── hybrid_search.py
│ ├── multi_query.py
│ ├── query_engine.py
│ └── context_compression.py
│
├── reranking/
│ └── reranker.py
│
├── llm/
│ └── generator.py
│
├── evaluation/
│ ├── generate_dataset.py
│ ├── evaluate_retrieval.py
│ └── evaluate_generation.py
│
├── utils/
│ └── logger.py
│
├── data/
│ ├── chunks/
│ │ ├── parents.json
│ │ └── chunks.json
│ │
│ ├── embeddings/
│ │ └── embeddings.npy
│ │
│ ├── index/
│ │ └── faiss.index
│ │
│ └── bm25/
│ └── bm25.pkl
│
└── main.py

⸻

Data Architecture

Parent chunk structure.

{
parent_id
text
page
source
}

Child chunk structure.

{
chunk_id
parent_id
text
page
source
}

Hierarchy.

Parent Chunk (~1000 tokens)

├─ Child Chunk (~300 tokens)
├─ Child Chunk
├─ Child Chunk
└─ Child Chunk

⸻

Ingestion Layer

Responsibilities:

PDF parsing
sentence segmentation
parent-child chunk creation
chunk storage

Flow.

PDF
↓
load_doc()
↓
build_parent_child_chunks()
↓
parents.json
chunks.json

Chunk parameters.

parent_tokens ≈ 1000
child_tokens ≈ 300
overlap ≈ 80

⸻

Embedding + Index Layer

Embeddings generated for child chunks only.

Model:

BAAI/bge-small-en-v1.5

Vector dimension.

384

Index:

FAISS IndexFlatIP (cosine similarity)

Additional index:

BM25 keyword index

Artifacts produced.

embeddings.npy
faiss.index
bm25.pkl

⸻

Retrieval Layer

Hybrid retrieval combines semantic and lexical search.

Process.

vector_search(query, k)
bm25_search(query, k)
↓
Reciprocal Rank Fusion
↓
hybrid_search(query)

Fusion algorithm.

RRF (k = 60)

⸻

Query Understanding Layer

Two LLM-driven transformations. 1. Query rewrite

user question
→ concise retrieval query

    2.	Query expansion

generate 3 alternate queries

Final search set.

[rewritten_query + expansion_queries]

⸻

Multi-Query Retrieval

Each query runs hybrid retrieval.

Results merged.

query_1 → results
query_2 → results
query_3 → results
query_4 → results

deduplicate by chunk_id

Output.

candidate chunks (~20)

⸻

Reranking Layer

Cross-encoder relevance model.

Model.

BAAI/bge-reranker-base

Input.

(query, chunk_text)

Output.

relevance score

Top results retained.

top_k = 7

⸻

Parent Expansion

Child chunks are expanded to their parent sections.

Purpose.

recover full context surrounding retrieved evidence

Process.

child chunks
↓
collect parent_id
↓
load parents.json
↓
retrieve parent text

⸻

Context Compression

Parent text is reduced using sentence-level ranking.

Model.

BAAI/bge-reranker-base

Process.

parent text
↓
sentence segmentation
↓
(query, sentence) scoring
↓
top sentences selected

Configuration.

sentences_per_parent ≈ 6

⸻

Prompt Construction

Context built from compressed parents.

Structure.

Documents:
<compressed context>

Question:
<user question>

Grounding rules.

Use only provided documents
Answer based on available information
Say "I don't know" only if no relevant information exists

⸻

LLM Layer

Local model via Ollama.

llama3

Interface.

POST http://localhost:11434/api/chat

Response returned to user.

⸻

Evaluation System

Two evaluation modes.

Retrieval evaluation.

Chunk Recall@3

Generation evaluation.

LLM-based scoring (1–5 scale)

Dataset generation.

LLM generates QA pairs from chunks
ground truth stored with chunk_id

Dataset structure.

{
question
expected_answer
chunk_id
source_page
}

⸻

Current Performance

Retrieval.

Chunk Recall@3 ≈ 0.98

Generation.

Average Answer Score ≈ 3.8–4.5

⸻

Technology Stack

Language.

Python

Core libraries.

sentence-transformers
faiss-cpu
rank-bm25
pypdf
nltk
tiktoken
numpy
torch
requests
orjson
tqdm

Models.

Embedding:
BAAI/bge-small-en-v1.5

Reranker:
BAAI/bge-reranker-base

LLM:
llama3 (Ollama)

Hardware.

Apple Silicon (M-series)
Torch MPS backend

⸻

Observability

Logging system tracks.

query rewrite
query expansion
retrieval candidates
reranking results
context preview
LLM response

⸻

System Characteristics

Capabilities.

document question answering
semantic + lexical retrieval
context-aware reasoning
evaluation benchmarking
local LLM operation

Limitations.

single-document knowledge base
no persistent vector DB
no multi-document ranking
no user interface
no streaming responses

⸻

Expansion Potential

This architecture supports extension to:

multi-document knowledge bases
API-based AI assistants
enterprise document search
legal / research assistants
personal knowledge agents
AI copilots

⸻

This specification fully describes the current system so it can be used as the baseline architecture for building a real-world RAG application.
