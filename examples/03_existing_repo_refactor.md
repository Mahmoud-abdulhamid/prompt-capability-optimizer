# Example 03: Existing Repository Refactoring

## 1. Raw User Input
```text
Refactor this project to improve architecture.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 2 (Architecture / Multi-File Refactor)
- **Primary Intent**: Systematically analyze current project coupling, eliminate circular dependencies, enforce clean domain layering, and preserve existing functionality under an additive change policy.
- **Discovered Capabilities**:
  - Code analysis, dependency graphs, AST refactoring.
  - Architecture standards: Clean Architecture / Hexagonal Architecture.
  - Test suites: Ensure regression prevention.
- **Output Mode**: Mode B (Optimize + Prepare with Phased Plan).

---

## 3. Optimized Prompt Output

```text
ROLE:
Staff Software Architect & Refactoring Specialist

OBJECTIVE:
Refactor the codebase to establish clean separation of concerns, eliminate code smells and tight coupling, and enhance maintainability while preserving 100% of existing behavior and public API contracts.

CONTEXT & REPOSITORY STATE:
- Inspection Target: Project root files (`package.json` / `pyproject.toml`, source tree, existing test suites).
- Baseline Rule: Do not modify existing tests initially; all tests must pass before and after refactoring.

CONSTRAINTS & SAFETY RULES:
- Additive & Incremental Policy: Refactor in isolated, commits/steps. Never attempt a blind whole-project rewrite.
- No Breaking Changes: Public function signatures, API routes, and exported types must remain backward-compatible.
- Zero Loss of Functionality: Every refactored module must maintain equivalent behavior.

REQUIRED CAPABILITIES & TOOLS:
- Native tools: `view_file`, `replace_file_content`, `run_command`
- Static Analysis: Linter and type checker to detect broken references immediately.

IMPLEMENTATION REQUIREMENTS:
1. Baseline Verification:
   - Run existing test suites and record test baseline status.
2. Architecture Boundary Definition:
   - Separate Presentation Layer (controllers/routes), Business Logic (services/domain models), and Infrastructure (DB/external clients).
3. Dependency Inversion:
   - Decouple high-level modules from low-level details using interfaces and dependency injection.
4. Eliminate Code Smells:
   - Remove circular imports, dead code, duplicated logic, and god objects (>300 lines).

EDGE CASES & RISKS:
- Side-effects during initialization (e.g., circular module imports causing undefined references at runtime).
- Hidden state mutations across shared singleton instances.

VERIFICATION PLAN:
- Baseline Test Pass: Ensure tests pass prior to touch.
- Continuous Typecheck: Run compiler after each refactored file.
- Regression Test Run: Full test suite execution (`npm test` or `pytest`).
- Lint & Style Check: Confirm project linting rules are strictly satisfied.

COMPLETION CRITERIA:
All existing tests pass with zero regressions, architectural layers are decoupled, and circular dependencies are eliminated.
```
