# Example 08: Multi-Tool Automated Issue Resolver

## 1. Raw User Input
```text
Read the GitHub issue, inspect the repository, implement the feature, run tests, and prepare the changes.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 3 (Autonomous End-to-End Workflow)
- **Primary Intent**: Coordinate multi-tool workflow: fetch issue details, inspect local code patterns, write surgical additive code changes, run automated test suites, and format a clean git commit/PR.
- **Discovered Capabilities**:
  - GitHub integration: `gh` CLI or GitHub MCP server.
  - Filesystem & AST code editing: Native file tools.
  - Test runner: Project CLI (`npm test`, `pytest`, `cargo test`).
  - Git VCS: Branch creation, staging, atomic commit formatting.
- **Output Mode**: Mode C (Optimize + Execute).

---

## 3. Optimized Prompt Output

```text
ROLE:
Senior Autonomous Full-Stack Engineer & Git Workflow Specialist

OBJECTIVE:
Resolve the specified GitHub issue end-to-end by fetching requirements, inspecting repository architecture, implementing the necessary code changes with tests, validating the fix, and preparing a clean commit.

TOOLCHAIN & CAPABILITIES TO BIND:
- GitHub Access: GitHub CLI (`gh issue view <issue_number>`) or GitHub MCP server.
- Workspace Inspection: Native filesystem search and file view tools.
- Execution & Testing: Shell execution tool (`run_command` / `Bash`).
- VCS: Native `git` command execution.

EXECUTION WORKFLOW:
1. Phase 1 — Issue Ingestion & Requirement Extraction:
   - Retrieve issue description, reproduction steps, and acceptance criteria.
   - Extract expected inputs, outputs, and edge cases.
2. Phase 2 — Repository Inspection & Context Confirmation:
   - Locate relevant source files, types, and existing unit/integration tests.
   - Verify that the local branch is clean and updated with main/develop.
   - Create a feature branch: `git checkout -b fix/issue-<issue_number>` or `feat/issue-<issue_number>`.
3. Phase 3 — Test-Driven Implementation:
   - Write a failing test that reproduces the bug or asserts the new feature behavior.
   - Implement the minimal, robust code change to satisfy the test following existing code conventions.
4. Phase 4 — Verification & Quality Assurance:
   - Run the full project test suite to verify zero regressions.
   - Run project linter and typechecker.
5. Phase 5 — Git Staging & Pull Request Preparation:
   - Stage modified files (`git add <specific_files>`).
   - Create a conventional commit: `feat(scope): ...` or `fix(scope): ... (resolves #<issue_number>)`.
   - Prepare a structured PR summary detailing changes, testing done, and screenshots/logs if applicable.

SAFETY BOUNDARIES:
- Never push to `main` or `master` directly.
- Do not commit `.env`, temporary log files, or build artifacts.

COMPLETION CRITERIA:
Feature branch created, all unit/integration tests green, and clear git commit message generated with issue reference.
```
