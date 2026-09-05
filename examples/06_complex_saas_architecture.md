# Example 06: Complex SaaS Architecture Design & Implementation

## 1. Raw User Input
```text
Design and implement a production-grade SaaS architecture.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 4 (Enterprise System / Multi-Service)
- **Primary Intent**: Design a secure, multi-tenant cloud-native SaaS architecture including tenancy isolation, RBAC/ABAC authorization, metering, billing webhooks, asynchronous background processing, and observability.
- **Discovered Capabilities**:
  - Multi-tenancy models (Shared DB / Separate Schema vs. Database per Tenant).
  - High availability and distributed messaging (PostgreSQL RLS, Redis queues, BullMQ/Kafka).
  - Billing & subscriptions (Stripe Webhook idempotency).
  - Distributed tracing & telemetry (OpenTelemetry, Prometheus metrics).
- **Output Mode**: Mode B (Phased Architectural Blueprint & Implementation).

---

## 3. Optimized Prompt Output

```text
ROLE:
Chief Cloud Architect & Enterprise Systems Engineer

OBJECTIVE:
Design and implement the core foundation of a production-grade multi-tenant B2B SaaS architecture, ensuring ironclad tenant data isolation, role-based access control, scalable background worker processing, and comprehensive observability.

CORE ARCHITECTURAL PILLARS:
1. Multi-Tenancy & Data Isolation:
   - Implement Tenant-per-Row isolation enforced at the database engine level using PostgreSQL Row-Level Security (RLS) with session variable injection (`SET LOCAL app.current_tenant_id = '...'`).
   - Every database query must automatically bind tenant context through scoped ORM middleware.
2. Authentication & Fine-Grained Authorization:
   - Tenant-aware authentication supporting SSO/SAML and passwordless magic links.
   - Granular RBAC (Owner, Admin, Member, Viewer) with permissions verified via custom decorators / guards.
3. Subscription & Usage Metering:
   - Subscription state machine integrated with Stripe billing.
   - Idempotent Stripe webhook receiver handling `customer.subscription.updated` and `invoice.payment_failed` with cryptographic signature verification.
4. Asynchronous Queue & Background Worker:
   - Distributed job queue (e.g., BullMQ backed by Redis) with retry backoff, concurrency throttling, and dead-letter queues (DLQ).
5. Observability & Auditing:
   - Structured JSON logging with correlation IDs (`trace_id`, `tenant_id`, `user_id`).
   - Comprehensive audit logging for all mutating tenant administrative actions.

PHASED IMPLEMENTATION PLAN:
- Phase 1: Database schema, tenant RLS policies, and Prisma/TypeORM tenant extension.
- Phase 2: Core authentication, JWT tenant claims, and RBAC authorization guards.
- Phase 3: Stripe webhook integration with idempotency keys.
- Phase 4: BullMQ background queue setup with error handling.
- Phase 5: Integration tests validating tenant isolation boundaries (ensuring Tenant A cannot access Tenant B data).

VERIFICATION MATRIX:
- Tenant Isolation Test: Explicit automated test asserting 0 rows returned when querying foreign tenant ID.
- Webhook Signature Test: Verifying replayed or unsigned payloads return 400 Bad Request.
- Concurrency Test: Validating background workers process jobs without race conditions.

COMPLETION CRITERIA:
Multi-tenant isolation verified with automated tests; core tenant onboarding and subscription webhooks fully operational.
```
