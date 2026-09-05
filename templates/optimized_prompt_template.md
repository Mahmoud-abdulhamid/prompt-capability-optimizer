# Optimized Prompt Master Template

Use this canonical template when generating final optimized prompts. Blocks that are not applicable to the specific task depth should be omitted cleanly without leaving empty placeholders.

---

```text
ROLE:
[Domain-specific Senior Engineer Persona, e.g., Senior Distributed Systems Engineer / Security Specialist]

OBJECTIVE:
[Single, crystal-clear, measurable objective specifying exactly what outcome must be produced]

CONTEXT & REPOSITORY STATE:
- Target Stack: [e.g., Node.js 20, TypeScript 5.4, Fastify, PostgreSQL 16]
- Existing Configuration: [e.g., tsconfig.json with strict: true, ESLint flat config]
- Key Files Identified: [e.g., src/server.ts, src/modules/auth/auth.service.ts]

CONSTRAINTS & NON-NEGOTIABLES:
- Additive Change Policy: Preserve existing working endpoints and shared types.
- Strict Typing: No 'any', explicit return types on all exported functions.
- Security Constraints: Zero secret logging, parameterized queries only, sanitize all untrusted input.
- Negative Constraints: Do NOT introduce new external libraries unless explicitly approved.

REQUIRED CAPABILITIES & TOOLS:
- Discovered Local Skills: [e.g., nestjs-development, api-security]
- Active MCP Tools: [e.g., PostgreSQL MCP, GitHub MCP]
- Native Agent Tools: [e.g., replace_file_content, run_command]

IMPLEMENTATION REQUIREMENTS:
1. Data Contracts & Schemas:
   - Define exact interfaces, DTOs, and validation schemas (e.g., Zod / class-validator).
2. Business Logic Execution:
   - Implement handlers with deterministic control flow, explicit timeouts, and idempotency keys.
3. Error Handling Architecture:
   - Handle all known failure modes with structured error payloads and correct HTTP status codes.

EDGE CASES & FAILURE MODES:
- Edge Case 1: [e.g., Network timeout during external payment gateway call -> Implement exponential backoff]
- Edge Case 2: [e.g., Concurrent database writes to duplicate key -> Catch unique constraint violation and return 409]
- Edge Case 3: [e.g., Malformed payload / unexpected types -> Return 400 with detailed validation errors]

VERIFICATION & TESTING PLAN:
- Static Analysis: [Exact command, e.g., npx tsc --noEmit && npm run lint]
- Unit / Integration Tests: [Exact command, e.g., npm test -- --coverage]
- Runtime Verification: [Exact command or curl check to verify service health]

COMPLETION CRITERIA:
- All new and existing automated tests pass with 0 errors and 0 warnings.
- No regression introduced in existing test suites.
- Production-grade code formatting applied.
```

---
**Author**: Mahmoud Abdelhameid ([LinkedIn](https://www.linkedin.com/in/mahmoud-abdelhameid-dev/) | [Email](mailto:Develper.net@gmail.com)) | **Copyright**: © 2026 Mahmoud Abdelhameid. All rights reserved. | **License**: MIT License
