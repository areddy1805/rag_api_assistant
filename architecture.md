RAG API Assistant — System Architecture

Overview

RAG API Assistant is a production-style Retrieval-Augmented Generation system designed to answer developer questions using API documentation.

The system ingests heterogeneous documentation sources (HTML, Markdown, OpenAPI specs, PDFs), builds hybrid retrieval indexes, and uses a large language model to generate grounded answers using retrieved context.

The architecture consists of six primary subsystems: 1. Document Ingestion 2. Query Understanding 3. Hybrid Retrieval 4. Context Construction 5. Answer Generation 6. Observability and Evaluation

⸻

1. High-Level Architecture

User Query
│
▼
Query Understanding
├ Query Rewrite
├ Query Expansion
├ Endpoint Extraction
├ Service Detection
└ Schema Detection
│
▼
Hybrid Retrieval
├ Vector Search (FAISS)
├ BM25 Search
├ Endpoint Search
└ Metadata Filtering
│
▼
Reciprocal Rank Fusion
│
▼
Cross-Encoder Reranking
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
Final Answer

⸻

2. Document Ingestion Pipeline

The ingestion pipeline converts raw documentation into a retrieval-optimized index.

Supported Sources
• HTML documentation
• Markdown documentation
• OpenAPI specifications
• PDF documents

Pipeline Steps

Raw Documents
│
▼
Document Loader
│
▼
Document Parsing
│
▼
Parent-Child Chunking
│
├ Parent documents
└ Child chunks
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
├ bm25/
└ index/

⸻

3. Query Understanding Layer

The query understanding layer transforms raw user queries into retrieval-optimized queries.

Capabilities
• Query rewriting
• Query expansion
• Endpoint extraction
• API service detection
• Schema query detection

Components

query_rewrite.py
query_expansion.py
endpoint_extractor.py
service_detector.py
schema_detector.py
query_entities.py

These steps improve retrieval recall and routing accuracy.

⸻

4. Hybrid Retrieval System

The retrieval layer combines multiple search strategies.

Retrieval Strategies

Vector Search
BM25 Keyword Search
Endpoint Index Search
Metadata Search

Vector search is implemented using FAISS with BGE embeddings.

BM25 is used for lexical matching of API terms and identifiers.

Result Fusion

Results are merged using Reciprocal Rank Fusion (RRF).

This improves recall while maintaining ranking stability.

⸻

5. Reranking

After retrieval, candidate documents are reranked using a cross-encoder model.

Model used:

BAAI/bge-reranker-base

The cross-encoder performs semantic pair scoring:

(query, document)

The top-k most relevant documents are selected for context construction.

⸻

6. Parent Document Expansion

Child chunks often lose surrounding context during chunking.

Parent expansion restores document context by retrieving the parent document of top-ranked chunks.

child chunk
│
▼
parent document

This increases answer completeness.

⸻

7. Contextual Compression

Parent documents may still be too large for LLM input.

Contextual compression selects the most relevant sentences from each parent document using a cross-encoder relevance model.

This step reduces token usage while preserving important information.

⸻

8. Token Budget Context Builder

The context builder enforces strict token limits before generation.

Parameters:

MAX_CONTEXT_TOKENS
MAX_CHUNK_TOKENS

Documents are truncated if necessary to ensure prompt size remains within model limits.

⸻

9. LLM Generation Layer

The generation layer produces the final answer using retrieved context.

Models Used

Qwen2.5 3B → query rewrite + expansion
Qwen2.5 7B → final answer generation

Generation supports both:
• standard responses
• streaming responses

⸻

10. Observability System

The system includes full RAG observability.

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

A tracing engine tracks timing across pipeline stages:

rewrite
expansion
retrieval
rerank
compression
generation

⸻

11. Evaluation Framework

The system includes an evaluation framework for measuring retrieval and generation quality.

Retrieval Metrics

Chunk Recall@K
Parent Recall@K

Generation Metrics

Grounding Score

Evaluation tools:

generate_dataset.py
evaluate_retrieval.py
evaluate_generation.py
analyze_retrieval_failures.py

⸻

12. API Layer

The system exposes a FastAPI service.

Endpoints

POST /chat
POST /retrieve
GET /metrics
GET /health

⸻

13. Storage Layer

Vector storage:

FAISS

Optional backend:

pgvector

BM25 index stored as serialized object.

⸻

14. Repository Structure

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

⸻

15. Design Goals

The architecture prioritizes:
• high retrieval accuracy
• grounded answers
• modular design
• observability
• extensibility

This design allows the system to scale from a local RAG prototype to a production retrieval service.
:::
