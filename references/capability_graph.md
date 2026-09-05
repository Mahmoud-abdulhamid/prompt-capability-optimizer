# Capability Graph & Taxonomy Specification

This document formalizes the **Capability Graph** engine of `prompt-capability-optimizer`. Rather than matching keywords superficially, the engine decomposes user tasks into an ontology of technical capabilities, then maps those capabilities to the optimal combination of local skills, MCP tools, and engineering patterns.

---

## 1. Capability Ontology Hierarchy

All software engineering tasks decompose into five primary capability domains:

```text
                               TASK INTENT
                                    │
       ┌──────────────┬─────────────┼─────────────┬──────────────┐
       ▼              ▼             ▼             ▼              ▼
[ Architecture ] [ Operations ] [ Security ] [ Data/State ] [ Quality/Test ]
       │              │             │             │              │
       ├─ Framework   ├─ CI/CD      ├─ Auth/RBAC  ├─ Relational  ├─ Unit tests
       ├─ Patterns    ├─ Docker     ├─ Encryption ├─ Key-Value   ├─ E2E/Integ
       ├─ Contracts   ├─ Cloud/IaC  ├─ Injection  ├─ Migrations  ├─ Static/Lint
       └─ Boundaries  └─ Monitor    └─ Audit      └─ Caching     └─ Benchmark
```

---

## 2. Dynamic Decomposition Rules

When a prompt is evaluated, the optimizer traverses the graph:

### Example Decomposition: "Build a real-time collaborative whiteboarding API"
```text
Goal: Real-time Whiteboarding API
 ├── [Data & State]
 │    ├── Capability: Ephemeral state synchronization
 │    │    └── Candidate: Redis Pub/Sub, WebSockets
 │    └── Capability: Durable board storage
 │         └── Candidate: PostgreSQL + JSONB or MongoDB
 ├── [Architecture & Protocol]
 │    ├── Capability: Bidirectional socket streaming
 │    │    └── Candidate: Socket.io, ws, or WebTransport
 │    └── Capability: Operational Transformation / CRDT
 │         └── Candidate: Yjs or Automerge algorithms
 ├── [Security]
 │    ├── Capability: Room-level authorization
 │    │    └── Candidate: JWT claims, tenant scoping
 │    └── Capability: DoS & Message flood protection
 │         └── Candidate: Token-bucket rate limiting
 └── [Quality Assurance]
      └── Capability: Concurrent socket load testing
           └── Candidate: Artillery or k6
```

---

## 3. Capability Matching & Graph Resolution

Once the capability nodes are extracted, the engine maps each node to available resources:

```text
Capability Node ───► 1. Exact Local Skill Match (Score: 10/10)
                 ───► 2. Active MCP Tool Match (Score: 9/10)
                 ───► 3. Verified Online Skill Registry Match (Score: 8/10)
                 ───► 4. Official Upstream Documentation Pattern (Score: 7/10)
                 ───► 5. Base LLM In-Context Domain Instruction (Score: 6/10)
```

---

## 4. Conflict Resolution & Dependency Graph

Tasks often involve mutually exclusive technical options (e.g., REST vs. gRPC, TypeORM vs. Prisma).

1. **Resolution Precedence**:
   - **User Explicit Choice**: Always honored as primary constraint.
   - **Existing Repository Dependency**: If `package.json` has `prisma`, do not introduce `typeorm`.
   - **Official Ecosystem Standard**: If starting from scratch, select the standard community tool (e.g., Fastify + Zod for high-throughput Node.js).

2. **Graph Pruning**:
   - Capabilities that add zero value to the primary objective are pruned.
   - Example: A request to "write an algorithmic sorter" does not need Docker, Kubernetes, or JWT auth capabilities.
