# Production Prompt Engineering Standards

This document establishes the rigorous engineering principles governing prompt transformation inside `prompt-capability-optimizer`.

---

## 1. The Core Law of Prompt Engineering

$$\text{Prompt Quality} = \frac{\text{Signal (Context + Constraints + Verification)}}{\text{Noise (Filler + Speculation + Redundancy)}}$$

A prompt must NEVER be expanded simply to make it longer. Every added word must directly constrain solution space, prevent common failure modes, or specify exact verification criteria.

---

## 2. Two-Pass Optimization Engine

### Pass 1: Semantic Clarification
1. **Disambiguate Jargon & Vague Verbs**:
   - Change *"make it secure"* to *"implement password hashing using Argon2id with m=65536, t=3, p=4, enforce HTTPS-only Secure/HttpOnly/SameSite=Strict cookies, and validate input with Zod schemas"*.
   - Change *"optimize it"* to *"reduce memory allocations by streaming responses in chunks of 64KB and index foreign key lookups"*.
2. **Contextual Anchoring**:
   - Pull repository realities: active framework versions, linting configs, folder layouts, and existing shared types.
3. **Explicit Negative Constraints**:
   - Explicitly list what the agent **MUST NOT** do (e.g., "Do not introduce third-party libraries without explicit reason", "Do not modify database schema migrations already committed").

### Pass 2: Execution Tooling & Environment Binding
1. **Bind Real Tools**:
   - If Vitest is installed, command: `npx vitest run path/to/test.spec.ts`.
   - If TypeScript is present, command: `npx tsc --noEmit`.
2. **Phased Milestones**:
   - Divide complex implementation into sequential, testable phases.
3. **Failure Recovery Instructions**:
   - Specify how the agent should react if a compiler error or test failure occurs (e.g., "Inspect the exact stack trace; do not suppress linter errors with `@ts-ignore`").

---

## 3. Structural Prompt Anatomy

Every fully optimized prompt follows this modular structure (omitting irrelevant blocks for simple tasks):

```text
ROLE:
[Precise persona with domain specialty, e.g., Senior Systems Engineer]

OBJECTIVE:
[Single-sentence, unambiguous definition of the primary target outcome]

CONTEXT & REPOSITORY REALITY:
[Actual files, languages, framework versions, and configurations identified]

CONSTRAINTS:
- Architectural constraints
- Library restrictions (Additive change policy)
- Typing standards (Strict TypeScript, zero `any`)

REQUIRED CAPABILITIES & TOOLS:
[Discovered skills, active MCP servers, native agent tools]

IMPLEMENTATION REQUIREMENTS:
- Step-by-step concrete specifications
- Data structures and schemas
- Method signatures and contracts

EDGE CASES & SECURITY BOUNDARIES:
- Error conditions and exceptions
- Sanitization and authorization rules
- Resource leak prevention (timeouts, closing handles)

VERIFICATION & TESTING DIRECTIVES:
- Exact build command: [e.g., npm run build]
- Exact test command: [e.g., npm test]
- Exact lint command: [e.g., npm run lint]

COMPLETION CRITERIA:
[Deterministic conditions required to consider the task complete]
```

---

## 4. Intent Preservation Rule

1. **Clarifying Intent (Required)**:
   - Defining edge cases, specifying HTTP status codes, supplying standard error formats, setting timeouts.
2. **Changing Intent (Strictly Forbidden)**:
   - Altering the user's choice of database, swapping language, replacing requested libraries, or adding unrequested feature scopes.
   - Any architectural suggestion not mandated by the user must be explicitly designated as:
     `RECOMMENDATION (Optional): ...`

---
**Author**: Mahmoud Abdelhameid ([LinkedIn](https://www.linkedin.com/in/mahmoud-abdelhameid-dev/) | [Email](mailto:Develper.net@gmail.com)) | **Copyright**: © 2026 Mahmoud Abdelhameid. All rights reserved. | **License**: MIT License
