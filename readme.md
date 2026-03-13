:::writing{variant=“standard” id=“67125”}

RAG API Assistant — Baseline Retrieval System

Overview

This repository contains the baseline implementation of a production-style Retrieval Augmented Generation (RAG) system designed for high-accuracy document question answering.

The system combines:
• hybrid retrieval (vector + lexical search)
• parent–child hierarchical chunking
• cross-encoder reranking
• sentence-level context compression

to produce grounded answers from document sources.

The architecture is intentionally transparent and modular so that each retrieval stage can be inspected, evaluated, and improved.

This repository represents Version 1 of the retrieval engine that will later evolve into a full Internal API Knowledge Assistant capable of indexing and querying large developer documentation corpora.

⸻

System Type

Retrieval Augmented Generation (RAG)

Pipeline type:

Hybrid Retrieval + Parent–Child Context Expansion + Sentence Compression

⸻

Purpose

Answer questions using document knowledge with:
• high retrieval recall
• strong contextual grounding
• minimal hallucination

The system retrieves relevant document sections and provides them as context to an LLM, ensuring answers remain grounded in source material.

⸻

High-Level Architecture

Documents
↓
Ingestion
↓
Parent–Child Chunking
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

Repository Structure

rag_v1/

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

The system uses hierarchical chunking.

Large document sections are stored as parent chunks, while smaller segments are indexed as child chunks.

Only child chunks are embedded and indexed.

Parent chunks are used later to recover broader context.

Parent Chunk

{
parent_id
text
page
source
}

Child Chunk

{
chunk_id
parent_id
text
page
source
}

Hierarchy

Parent (~1000 tokens)

├ Child (~300 tokens)
├ Child
├ Child
└ Child

⸻

Ingestion Layer

The ingestion pipeline converts source documents into indexed chunks.

Responsibilities:
• PDF parsing
• sentence segmentation
• parent–child chunk generation
• artifact persistence

Processing Flow

PDF
↓
load_doc()
↓
build_parent_child_chunks()
↓
parents.json
chunks.json

Chunk Configuration

parent_tokens ≈ 1000
child_tokens ≈ 300
overlap ≈ 80

⸻

Embedding and Index Layer

Embeddings are generated only for child chunks.

Embedding Model

BAAI/bge-small-en-v1.5

Embedding Dimension

384

Vector Index

FAISS IndexFlatIP

This configuration performs cosine similarity search.

Additional Index

BM25 lexical index

Generated Artifacts

embeddings.npy
faiss.index
bm25.pkl

⸻

Retrieval Pipeline

The system uses hybrid retrieval, combining semantic and lexical search.

Retrieval Process

vector_search(query, k)
bm25_search(query, k)
↓
Reciprocal Rank Fusion
↓
hybrid_search(query)

Fusion Algorithm

Reciprocal Rank Fusion

RRF constant k = 60

⸻

Query Understanding

The system improves search quality using two LLM-driven transformations.

Query Rewrite

The user question is converted into a concise retrieval query.

User Question
↓
Rewrite
↓
Optimized Search Query

Query Expansion

The system generates additional alternative queries.

Original Query

- 3 Expanded Queries

Final Query Set

[ rewritten_query + expansion_queries ]

⸻

Multi-Query Retrieval

Each query variant executes the hybrid retrieval pipeline.

query_1 → results
query_2 → results
query_3 → results
query_4 → results

Results are merged and deduplicated by chunk_id.

Output

candidate chunks ≈ 20

⸻

Reranking Layer

Candidate chunks are reranked using a cross-encoder relevance model.

Model

BAAI/bge-reranker-base

Input

(query, chunk_text)

Output

Relevance score.

Selection

top_k = 7

⸻

Parent Context Expansion

Child chunks contain limited context.

The system retrieves the corresponding parent chunk to restore the surrounding section.

Process

child chunks
↓
collect parent_id
↓
load parents.json
↓
retrieve parent text

⸻

Context Compression

Parent chunks may be too large for LLM prompts.

The system compresses them using sentence-level ranking.

Model

BAAI/bge-reranker-base

Compression Pipeline

parent text
↓
sentence segmentation
↓
score(query, sentence)
↓
select top sentences

Configuration

sentences_per_parent ≈ 6

⸻

Prompt Construction

The final prompt is constructed from compressed document context.

Prompt Structure

Documents:
<compressed context>

Question:
<user question>

Grounding Rules
• Use only the provided documents
• Base answers strictly on retrieved context
• If no information exists, return:

"I don't know"

⸻

LLM Layer

Generation currently runs locally.

Model

llama3

Runtime

Ollama

Endpoint

POST http://localhost:11434/api/chat

⸻

Evaluation System

The system includes automated evaluation for both retrieval and generation.

Retrieval Evaluation

Metric:

Chunk Recall@3

Measures whether relevant chunks are retrieved.

Generation Evaluation

Answers are scored using LLM-based grading.

Score range:

1 – 5

Dataset Generation

The evaluation dataset is generated automatically.

Process:
• LLM creates QA pairs from document chunks
• Ground truth chunk IDs are recorded

Dataset Format

{
question
expected_answer
chunk_id
source_page
}

⸻

Current Performance

Retrieval

Chunk Recall@3 ≈ 0.98

Generation

Average Answer Score ≈ 3.8 – 4.5

⸻

Technology Stack

Language

Python

Core Libraries

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

Models

Embedding

BAAI/bge-small-en-v1.5

Reranker

BAAI/bge-reranker-base

LLM

llama3 (Ollama)

Hardware

Apple Silicon (M-series)
Torch MPS backend

⸻

Observability

The system logs the following information for each query.

query rewrite
query expansion
retrieval candidates
reranking results
context preview
LLM response

This enables debugging and retrieval quality analysis.

⸻

System Capabilities

Current capabilities:
• document question answering
• hybrid semantic + lexical retrieval
• context-aware reasoning
• automated evaluation
• local LLM inference

⸻

Current Limitations

The current baseline system has several limitations.

single-document knowledge base
no persistent vector database
no multi-document ranking
no API service
no streaming responses
no UI interface

⸻

Future Expansion

This architecture is designed to evolve into a developer documentation intelligence system.

Future extensions include:

multi-document knowledge bases
API documentation assistants
enterprise developer search
RAG-powered internal copilots
large documentation indexing
production API service

⸻

Project Status

Current state:

Baseline RAG Retrieval System

This version serves as the foundation for building a production-grade developer documentation assistant.
:::
