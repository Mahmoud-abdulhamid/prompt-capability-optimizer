# Example 07: Research & Comparative RAG Evaluation

## 1. Raw User Input
```text
Compare the best approaches for implementing RAG in this project.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 4 (Research & Technical Evaluation)
- **Primary Intent**: Conduct an objective, engineering-driven trade-off analysis comparing Retrieval-Augmented Generation (RAG) architectures specifically for this project's scale, latency budget, data formats, and tech stack.
- **Discovered Capabilities**:
  - Vector stores: pgvector, Qdrant, Pinecone, Milvus.
  - Embedding models & chunking strategies: Semantic chunking, recursive character chunking, token sizing.
  - Retrieval strategies: Hybrid search (BM25 + Dense vector), Cohere reranking, Parent Document Retrieval, Hypothetical Document Embeddings (HyDE).
  - Evaluation metrics: Ragas framework (Faithfulness, Answer Relevance, Context Precision, Context Recall).
- **Output Mode**: Mode A (Research Decision Matrix).

---

## 3. Optimized Prompt Output

```text
ROLE:
Principal AI/ML Systems Engineer & Information Retrieval Specialist

OBJECTIVE:
Produce an evidence-based technical evaluation report comparing the optimal RAG (Retrieval-Augmented Generation) architectures tailored to the current repository's stack, data characteristics, and operational constraints.

ANALYSIS DIMENSIONS & TRADEOFF MATRIX:
Evaluate RAG approaches across the following core dimensions:
1. Storage & Vector Indexing:
   - Option A: PostgreSQL with `pgvector` (HNSW vs. IVFFlat indexing).
   - Option B: Dedicated Vector DB (e.g., Qdrant / Pinecone).
   - Metrics: Operational complexity, query latency at $10^5$ vs. $10^7$ vectors, memory overhead, transactional consistency.
2. Ingestion & Chunking Optimization:
   - Fixed-size token window with overlap vs. Markdown/AST structural chunking vs. Semantic chunking.
   - Metadata extraction strategies to enable pre-filtering (e.g., by tenant, date, document type).
3. Retrieval & Ranking Architecture:
   - Pure semantic search vs. Hybrid Search (reciprocal rank fusion of sparse BM25 + dense embeddings).
   - Impact of secondary cross-encoder re-ranking (e.g., Cohere or BGE-reranker) on precision vs. p99 latency.
4. Latency & Cost Modeling:
   - Projected monthly embedding/inference cost across traffic tiers (10k, 100k, 1M queries/mo).
   - End-to-end p95 response time breakdown (embedding + vector search + reranking + LLM synthesis).
5. Evaluation & Drift Monitoring:
   - Automated quality benchmarking methodology using the Ragas or TruLens framework.

OUTPUT DELIVERABLE:
1. Executive Decision Matrix: Structured comparative table scoring options from 1-10 on Latency, Cost, Accuracy, and Maintenance.
2. Concrete Stack Recommendation: Clear, justified selection for this project.
3. Minimal Proof-of-Concept Implementation Plan: Step-by-step architecture blueprint to deploy the recommended pipeline.

COMPLETION CRITERIA:
Deliverable provides actionable architectural certainty grounded in empirical metrics; avoids generic marketing claims.
```
