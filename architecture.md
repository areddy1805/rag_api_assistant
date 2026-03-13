1.  High-Level Architecture

                        ┌─────────────────────────────┐
                        │         Client Apps         │
                        │  (CLI / UI / Slack / Web)   │
                        └──────────────┬──────────────┘
                                       │
                                HTTP / REST
                                       │
                         ┌─────────────▼─────────────┐
                         │        FastAPI Server      │
                         │         backend/api        │
                         └─────────────┬─────────────┘
                                       │
                        ┌──────────────▼──────────────┐
                        │        Query Service         │
                        │  (retrieval orchestration)   │
                        └──────────────┬──────────────┘
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
        ┌────────▼────────┐  ┌─────────▼─────────┐  ┌────────▼────────┐
        │ Query Understanding │  │ Retrieval Engine │  │ Reranking Engine │
        │ rewrite + expansion │  │ hybrid retrieval │  │ cross encoder   │
        └────────┬─────────┘  └─────────┬─────────┘  └────────┬────────┘
                 │                      │                     │
                 │                      ▼                     │
                 │            Parent Context Expansion       │
                 │                      │                     │
                 │                      ▼                     │
                 │              Sentence Compression         │
                 │                      │                     │
                 └──────────────► Context Builder ◄──────────┘
                                       │
                                       ▼
                               LLM Generation
                                       │
                                       ▼
                                 Final Answer

---

              DATA PLATFORM LAYER

        ┌─────────────────────────────────────┐
        │         Ingestion Pipelines         │
        │ HTML / Markdown / PDF / OpenAPI     │
        └─────────────────────────────────────┘
                       │
                       ▼
             Document Normalization
                       │
                       ▼
            Parent-Child Chunking Engine
                       │
                       ▼
              Metadata Enrichment
                       │
                       ▼
               Embedding Generation
                       │
                       ▼
             Vector Store + BM25 Index
                       │
                       ▼
                   Retrieval Core

---

            PLATFORM INFRASTRUCTURE LAYER

        Configuration
        Observability (logs / metrics)
        Evaluation framework
        Dataset management

⸻

2. Final Directory Structure

Production-style repository layout.

rag_api_assistant/

├── backend/
│
│ ├── api/
│ │ ├── server.py
│ │ ├── routes/
│ │ │ ├── chat.py
│ │ │ ├── retrieve.py
│ │ │ ├── health.py
│ │ │ └── metrics.py
│ │ └── schemas.py
│
│ ├── config/
│ │ ├── settings.py
│ │ ├── logging_config.py
│ │ └── constants.py
│
│ ├── ingestion/
│ │
│ │ ├── loaders/
│ │ │ ├── html_loader.py
│ │ │ ├── markdown_loader.py
│ │ │ ├── pdf_loader.py
│ │ │ ├── openapi_loader.py
│ │ │ └── json_loader.py
│ │
│ │ ├── parsers/
│ │ │ ├── html_parser.py
│ │ │ ├── markdown_parser.py
│ │ │ └── openapi_parser.py
│ │
│ │ ├── chunking/
│ │ │ ├── semantic_chunk.py
│ │ │ ├── parent_child_chunker.py
│ │ │ └── sentence_splitter.py
│ │
│ │ ├── metadata/
│ │ │ ├── metadata_extractor.py
│ │ │ └── schema_metadata.py
│ │
│ │ ├── embedding/
│ │ │ └── embedding_generator.py
│ │
│ │ └── pipeline.py
│
│ ├── retrieval/
│ │
│ │ ├── core/
│ │ │ ├── vector_search.py
│ │ │ ├── bm25_search.py
│ │ │ ├── hybrid_search.py
│ │ │ └── multi_query.py
│ │
│ │ ├── ranking/
│ │ │ └── reranker.py
│ │
│ │ ├── compression/
│ │ │ └── context_compression.py
│ │
│ │ ├── parent_expansion/
│ │ │ └── parent_retriever.py
│ │
│ │ ├── query_understanding/
│ │ │ ├── query_rewrite.py
│ │ │ ├── query_expansion.py
│ │ │ └── query_classifier.py
│ │
│ │ └── query_engine.py
│
│ ├── vectorstore/
│ │ ├── vector_interface.py
│ │ ├── faiss_store.py
│ │ ├── pgvector_store.py
│ │ └── metadata_store.py
│
│ ├── llm/
│ │ ├── generator.py
│ │ ├── prompts.py
│ │ └── model_router.py
│
│ ├── evaluation/
│ │ ├── dataset_generation.py
│ │ ├── retrieval_eval.py
│ │ ├── generation_eval.py
│ │ └── metrics.py
│
│ ├── observability/
│ │ ├── logging.py
│ │ ├── tracing.py
│ │ └── metrics.py
│
│ ├── utils/
│ │ ├── text_utils.py
│ │ ├── file_utils.py
│ │ └── tokenizer.py
│
│ └── services/
│ ├── chat_service.py
│ └── retrieval_service.py
│
├── data/
│ ├── raw_docs/
│ ├── processed_docs/
│ ├── parents.json
│ ├── chunks.json
│ └── metadata.json
│
├── index/
│ ├── faiss.index
│ └── bm25.pkl
│
├── embeddings/
│ └── embeddings.npy
│
├── scripts/
│ ├── run_ingestion.py
│ ├── rebuild_index.py
│ └── run_evaluation.py
│
├── tests/
│ ├── retrieval_tests.py
│ ├── ingestion_tests.py
│ └── api_tests.py
│
├── pyproject.toml
├── .env
├── README.md
└── docker/
├── Dockerfile
└── docker-compose.yml

⸻

3. Module Responsibility Breakdown

API Layer

backend/api

Responsibilities:

Expose RAG system as a service.

Endpoints:

POST /chat
POST /retrieve
GET /health
GET /metrics

⸻

Services Layer

backend/services

Application orchestration layer.

chat_service
orchestrates full RAG pipeline

retrieval_service
runs retrieval without generation

⸻

Retrieval Core

backend/retrieval

Wraps existing baseline modules.

Existing modules preserved:

vector_search
bm25_search
hybrid_search
multi_query
reranker
context_compression

New orchestration:

query_engine.py

Flow:

user_query
→ query_rewrite
→ query_expansion
→ multi_query_retrieval
→ hybrid_search
→ reranker
→ parent_expansion
→ context_compression

⸻

Vector Store Layer

backend/vectorstore

Provides storage abstraction.

Allows switching storage engines.

Supported:

FAISS
pgvector
future: Pinecone / Weaviate

Interface example:

class VectorStore:

    def add_documents()

    def search()

    def delete()

    def update()

⸻

Ingestion System

backend/ingestion

Responsible for transforming raw documentation.

Pipeline:

load document
→ parse
→ clean
→ semantic segmentation
→ parent-child chunking
→ metadata extraction
→ embeddings
→ index storage

⸻

LLM Layer

backend/llm

Responsibilities:

query rewrite
query expansion
answer generation
evaluation scoring

Models:

local llama
Gemini 1.5
future models

⸻

Observability

backend/observability

Captures system telemetry.

Logs:

query rewrite output
retrieved chunks
reranker scores
selected documents
LLM latency
retrieval latency
token usage

Structured JSON logging.

⸻

Evaluation

backend/evaluation

Metrics:

Recall@k
Precision@k
Faithfulness
Answer correctness
Citation coverage

Dataset versioning supported.

⸻

4. Dependency List

Core ML stack:

sentence-transformers
faiss-cpu
rank-bm25
numpy
scikit-learn

LLM stack:

ollama
google-generativeai
tiktoken

API:

fastapi
uvicorn
pydantic

Document processing:

beautifulsoup4
markdown
pdfminer.six
pyyaml

Utilities:

python-dotenv
loguru
tenacity
tqdm

Evaluation:

datasets
pandas

⸻

5. Example pyproject.toml

[project]
name = "rag-api-assistant"
version = "0.1.0"

dependencies = [
"fastapi",
"uvicorn",
"pydantic",
"numpy",
"faiss-cpu",
"rank-bm25",
"sentence-transformers",
"beautifulsoup4",
"markdown",
"pdfminer.six",
"python-dotenv",
"loguru",
"tqdm",
"google-generativeai",
"ollama",
]

⸻

6. Configuration System Design

Centralized configuration.

backend/config/settings.py

Uses:

pydantic BaseSettings

Example:

class Settings(BaseSettings):

    VECTOR_STORE: str = "faiss"

    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"

    RERANKER_MODEL: str = "BAAI/bge-reranker-base"

    LLM_PROVIDER: str = "ollama"

    FAISS_INDEX_PATH: str = "./index/faiss.index"

    BM25_INDEX_PATH: str = "./index/bm25.pkl"

    CHUNK_SIZE_PARENT: int = 1000

    CHUNK_SIZE_CHILD: int = 300

⸻

7. Environment Variables

LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3
GOOGLE_API_KEY=
VECTOR_STORE=faiss

FAISS_INDEX_PATH=index/faiss.index
BM25_INDEX_PATH=index/bm25.pkl

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
RERANKER_MODEL=BAAI/bge-reranker-base

LOG_LEVEL=INFO

⸻

8. FastAPI Service Layout

backend/api/server.py

app = FastAPI()

include_router(chat_router)
include_router(retrieve_router)
include_router(health_router)
include_router(metrics_router)

Example endpoint:

POST /chat

{
"question": "How does the Stripe payment API work?"
}

Response:

{
"answer": "...",
"sources": [
{
"source": "Stripe Docs",
"section": "Create Payment Intent"
}
]
}

⸻

9. Ingestion Pipeline Architecture

run_ingestion.py

Pipeline:

load documents
↓
parse structure
↓
extract metadata
↓
semantic segmentation
↓
parent child chunking
↓
embedding generation
↓
vector index update
↓
bm25 index update

Supports loaders:

HTML docs
Markdown docs
PDF docs
OpenAPI specs
JSON examples

⸻

10. Vector Store Abstraction

Interface:

vector_interface.py

class VectorStore(ABC):

    def add_documents()

    def search()

    def delete()

    def save()

    def load()

Implementation:

faiss_store.py
pgvector_store.py

Retrieval core interacts only with interface.

Allows replacing FAISS later without changing retrieval pipeline.

⸻

11. Migration Plan From Baseline Repository

Step 1 — Move existing modules.

rag_v1/retrieval
→ backend/retrieval/core

Step 2 — Move reranker.

rag_v1/reranking/reranker.py
→ backend/retrieval/ranking

Step 3 — Move compression.

rag_v1/context_compression.py
→ backend/retrieval/compression

Step 4 — Move ingestion scripts.

rag_v1/ingestion
→ backend/ingestion

Step 5 — Move evaluation.

rag_v1/evaluation
→ backend/evaluation

Step 6 — Create orchestration layer.

query_engine.py

Step 7 — Create FastAPI server.

backend/api/server.py

Step 8 — Introduce vectorstore abstraction.

Wrap FAISS.

Step 9 — Add configuration system.

Step 10 — Add observability.

⸻

Production outcome:

multi-document ingestion
API server
modular retrieval engine
pluggable vector store
observability
evaluation framework
extensible ingestion system

This architecture mirrors internal AI infrastructure used in production RAG platforms.
