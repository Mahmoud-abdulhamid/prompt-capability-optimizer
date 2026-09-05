# Verification Matrix & Test Gate Template

This template structures the concrete testing and verification directives embedded into optimized prompts.

---

```markdown
## 🧪 Verification & Quality Gate Matrix

| Verification Layer | Target Scope | Command / Tool | Success Assertion Criteria |
| :--- | :--- | :--- | :--- |
| **Syntax & Linting** | All modified files | `npm run lint` / `ruff check .` | 0 errors, 0 warnings. Clean formatting. |
| **Type Integrity** | Full workspace | `npx tsc --noEmit` / `mypy .` | Zero type errors. Strict mode enforced. |
| **Unit Testing** | New functions & classes | `npm test -- <test_file>` | 100% assertions pass. Code paths covered. |
| **Integration Testing**| API & DB interactions | `npm run test:e2e` / `pytest tests/e2e` | Endpoints respond with valid payloads and codes. |
| **Security Analysis** | Input & Auth boundaries | Static checks + payload audits | Zero SQL/NoSQL injection, zero exposed secrets. |
| **Regression Check** | Existing test suite | Full project test runner | Baseline passes with no breaking changes. |

### Failure Recovery Directives:
1. If **TypeCheck fails**: Inspect interface mismatches directly. Never use `any` or `@ts-ignore` to silence errors.
2. If **Tests fail**: Read test output and failure diffs. Fix the underlying implementation logic, not the test assertions (unless the test itself contained flawed assumptions).
3. If **Linter fails**: Automatically fix formatting using project linter configs (`npm run lint -- --fix`).
```

---
**Author**: Mahmoud Abdelhameid ([LinkedIn](https://www.linkedin.com/in/mahmoud-abdelhameid-dev/) | [Email](mailto:Develper.net@gmail.com)) | **Copyright**: © 2026 Mahmoud Abdelhameid. All rights reserved. | **License**: MIT License
