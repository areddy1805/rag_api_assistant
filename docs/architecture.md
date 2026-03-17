RAG API Assistant — System Architecture

Overview

RAG API Assistant is a modular Retrieval-Augmented Generation (RAG) system designed to answer developer questions using API documentation. The system ingests heterogeneous documentation sources, builds hybrid retrieval indexes, and generates grounded answers using large language models.

The architecture follows a production-style RAG pipeline with strong emphasis on retrieval quality, observability, and evaluation.

Core Subsystems

1. Document Ingestion
2. Query Understanding
3. Hybrid Retrieval
4. Ranking and Context Construction
5. Answer Generation
6. Observability
7. Evaluation Framework
8. API Layer
9. Storage Layer

---

1. High-Level System Flow

User Query
│
▼
Query Understanding
│
▼
Multi-Query Retrieval
│
▼
Hybrid Search
│
▼
Reciprocal Rank Fusion
│
▼
Cross Encoder Reranking
│
▼
Parent Document Expansion
│
▼
Contextual Compression
│
▼
Token Budget Context Builder
│
▼
LLM Generation
│
▼
Grounding Validation
│
▼
Final Answer

---

2. Document Ingestion Pipeline

The ingestion pipeline converts raw documentation into a retrieval-optimized index.

Supported Sources

• HTML documentation
• Markdown documentation
• OpenAPI specifications
• PDF documents

Pipeline

Raw Documents
│
▼
Loader Router
│
▼
Format Specific Loaders
│
├ HTML Loader
├ Markdown Loader
├ OpenAPI Loader
└ PDF Loader
│
▼
Document Parsing
│
▼
Parent Child Chunking
│
├ Parent Documents
└ Child Chunks
│
▼
Embedding Generation
│
▼
Index Construction

Outputs

data/
├ processed_docs/
│ ├ chunks.json
│ └ parents.json
├ embeddings/
│ └ embeddings.npy
├ bm25/
│ └ bm25.pkl
└ index/
└ faiss.index

Parents preserve document context while children enable precise retrieval.

---

3. Query Understanding Layer

User queries are transformed into retrieval-optimized forms.

Capabilities

• Query rewriting
• Query expansion
• Endpoint extraction
• API service detection
• Schema query detection
• Entity extraction

Components

backend/retrieval/query_understanding/

query_rewrite.py
query_expansion.py
endpoint_extractor.py
service_detector.py
schema_detector.py
query_entities.py

Purpose

Improve recall and ensure correct retrieval routing.

---

4. Hybrid Retrieval System

The retrieval layer combines multiple search strategies.

Retrieval Methods

Vector Search

Semantic retrieval using embeddings.

Model

BAAI/bge-small-en-v1.5

Vector index

FAISS

BM25 Search

Lexical search for identifiers and API keywords.

Endpoint Search

Direct lookup for API endpoints.

Metadata Search

Filters results based on detected service or entities.

---

5. Result Fusion

Results from multiple retrieval methods are merged using Reciprocal Rank Fusion (RRF).

RRF advantages

• stable ranking
• improved recall
• robust against noisy signals

This produces a candidate set of documents for reranking.

---

6. Cross Encoder Reranking

Candidate documents are reranked using a cross encoder.

Model

BAAI/bge-reranker-base

Input

(query, document)

Output

semantic relevance score

Top-k results are selected for context construction.

---

7. Parent Document Expansion

Child chunks lack surrounding context.

Parent expansion restores document context.

child chunk
│
▼
parent document

This improves answer completeness and coherence.

---

8. Contextual Compression

Parent documents may exceed token limits.

Compression selects the most relevant sentences using a cross encoder relevance model.

Process

parent document
│
▼
sentence scoring
│
▼
top sentences
│
▼
compressed context

Benefits

• reduced token usage
• preserved semantic relevance

---

9. Token Budget Context Builder

Context must respect LLM input limits.

Two limits are enforced.

MAX_CONTEXT_TOKENS  
MAX_CHUNK_TOKENS

Chunks are truncated if necessary.

Goal

maximize relevant information within token budget.

---

10. Generation Layer

The LLM generation layer produces final answers.

Models

Query Rewrite + Expansion

Qwen2.5 3B

Answer Generation

Qwen2.5 7B

Features

• standard responses
• streaming responses
• context grounded prompts

---

11. Grounding Validation

Generated answers are validated against retrieved context.

Metric

Grounding Score

The score measures how much of the answer is supported by retrieved context.

Low scores trigger hallucination warnings.

---

12. Observability System

The system includes full RAG pipeline tracing.

Metrics Captured

query
rewrite
expansions
retrieved chunks
reranked chunks
context tokens
generation latency
token usage
grounding score

Tracing

rewrite
expansion
retrieval
rerank
parent_expansion
compression
context_builder
generation

Logs

logs/rag.log

---

13. Evaluation Framework

The repository includes an offline evaluation system.

Retrieval Metrics

Chunk Recall@K  
Parent Recall@K

Generation Metrics

LLM Judge Score  
Grounding Score

Tools

backend/evaluation/

generate_dataset.py  
evaluate_retrieval.py  
evaluate_generation.py  
analyze_retrieval_failures.py  
retrieval_diagnostics.py

These tools allow systematic RAG benchmarking.

---

14. API Layer

The system exposes a FastAPI service.

Endpoints

POST /chat  
POST /retrieve  
GET /metrics  
GET /health

Chat endpoint supports streaming responses.

---

15. Storage Layer

Vector storage

FAISS

Optional backend

pgvector

BM25 index

Serialized object

Document metadata

JSON store

---

16. Repository Structure

backend/
├ api/
├ config/
├ evaluation/
├ ingestion/
├ llm/
├ observability/
├ retrieval/
├ services/
└ vectorstore/

data/
├ raw_docs/
├ processed_docs/
├ embeddings/
├ bm25/
└ index/

docker/
scripts/
tests/

---

17. Design Principles

The architecture prioritizes

• retrieval accuracy
• grounded generation
• modular system design
• strong observability
• extensibility

The design allows scaling from a local RAG prototype to a production retrieval service.
