# Example 02: Coding & API Generation

## 1. Raw User Input
```text
Build a REST API using NestJS.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 2 (Complex / Feature Implementation)
- **Primary Intent**: Scaffold and implement a production-ready RESTful service using the NestJS framework with modular architecture, request validation, database connection, and automated tests.
- **Discovered Capabilities**:
  - NestJS Framework architecture (Controllers, Services, Modules).
  - Validation: `class-validator`, `class-transformer`, ValidationPipe.
  - Database: Prisma or TypeORM with PostgreSQL.
  - Testing: Jest unit and supertest e2e.
- **Selected Local Skills**: `nestjs-development` (Utility: 9.2), `api-security` (Utility: 8.8).
- **Output Mode**: Mode B (Optimize + Prepare).

---

## 3. Optimized Prompt Output

```text
ROLE:
Principal Backend Architect specializing in NestJS and enterprise Node.js microservices.

OBJECTIVE:
Build a modular, production-ready REST API in NestJS following official architectural patterns, featuring robust schema validation, database integration, structured error handling, and end-to-end tests.

CONTEXT & REPOSITORY REALITY:
- Runtime: Node.js 20+ / TypeScript 5.4+
- Framework: NestJS 10.x with Fastify or Express adapter
- Configuration: Strict TypeScript (`strict: true`, `noImplicitAny: true`)

CONSTRAINTS:
- Follow strict NestJS dependency injection and module boundaries.
- No business logic inside Controllers; Controllers solely handle HTTP serialization and routing.
- All request payloads must be strictly validated with DTOs using class-validator and class-transformer with `whitelist: true` and `forbidNonWhitelisted: true`.
- Never return raw database errors or stack traces to API clients.

REQUIRED CAPABILITIES & TOOLS:
- Native tools: `replace_file_content`, `write_to_file`, `run_command`
- Database tool: Prisma ORM / PostgreSQL migration engine
- Testing framework: Jest + Supertest

IMPLEMENTATION REQUIREMENTS:
1. Module Architecture:
   - Create feature module(s) containing: `*.module.ts`, `*.controller.ts`, `*.service.ts`, `dto/*.dto.ts`, and `entities/*.entity.ts`.
2. CRUD Operations & RESTful Conventions:
   - POST /resource (201 Created with Location header)
   - GET /resource (200 OK with pagination: page, limit, total)
   - GET /resource/:id (200 OK or 404 Not Found)
   - PATCH /resource/:id (200 OK or 404 Not Found)
   - DELETE /resource/:id (204 No Content or 404 Not Found)
3. Global Interceptors & Filters:
   - Global `HttpExceptionFilter` for uniform JSON error responses: `{ statusCode, timestamp, path, message }`.
   - Logging interceptor measuring execution time.

EDGE CASES & SECURITY:
- Handle database connection loss gracefully with health check endpoint (`/health`).
- Enforce UUID / integer format validation on route parameters using `ParseUUIDPipe` or `ParseIntPipe`.
- Apply Rate Limiting using `@nestjs/throttler` (e.g., 100 req/min).

VERIFICATION & TESTING PLAN:
- Unit Tests: Test service methods in isolation with mocked repository layer (`npm run test`).
- E2E Tests: Supertest suite against test database testing HTTP status codes (`npm run test:e2e`).
- Typecheck & Lint: `npm run lint && npx tsc --noEmit`.

COMPLETION CRITERIA:
API starts with zero runtime warnings, all endpoints pass e2e tests, and zero linter/type errors exist.
```
