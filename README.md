# Prompt Capability Optimizer (`prompt-capability-optimizer`)

> **Production-Grade, Cross-Platform Agent Meta-Skill for Intelligent Capability Discovery & Two-Pass Prompt Engineering**

`prompt-capability-optimizer` sits between a user's raw prompt and an AI coding agent's execution loop. It combines the active discovery principles of `find-skills` with modern engineering standards to generate mathematically sound, tool-aware, verified, and secure prompts.

---

## Key Features

- **Cross-Agent Compatibility**: Runs seamlessly on Claude Code, Gemini CLI, Cursor, Windsurf, Cline, Roo Code, Codex, and OpenCode.
- **Local & Online Discovery**: Auto-detects local skills across project/user paths and targets authoritative online registries (`skills.sh`).
- **Capability Graph & Scoring**: Evaluates candidate tools using a weighted utility formula and eliminates redundant skills to preserve context window.
- **Strict Security Boundaries**: Enforces the "Never Install Blindly" rule, prompt injection resistance, and zero plaintext secret leakage.
- **Two-Pass Optimization**:
  - **Pass 1 (Semantic)**: Clarifies requirements, bounds, and edge cases while strictly preserving user intent.
  - **Pass 2 (Execution)**: Binds real environment tools, linter/test directives, and execution phases.
- **Verification Gates**: Generates deterministic test commands (`tsc`, linters, unit/e2e tests) and runs an internal 13-point self-critique.

---

## Directory Structure

```text
.
├── SKILL.md                              # Main agent skill entry point & instructions
├── README.md                             # Project overview and installation guide
├── adapters/
│   ├── host_capabilities.json          # Standard JSON schema for host environment probing
│   └── environment_adapters.md          # Multi-agent adaptation and graceful fallback guide
├── references/
│   ├── capability_graph.md              # Technical taxonomy and decomposition graph
│   ├── prompt_engineering_standards.md # Two-level engineering principles and prompt anatomy
│   ├── scoring_rubric.md                # Mathematical scoring formulas and deduplication
│   ├── security_and_trust.md            # Installation governance and prompt injection guards
│   └── cross_agent_matrix.md            # Command Rosetta Stone across agent platforms
├── templates/
│   ├── optimized_prompt_template.md     # Standard template for optimized outputs
│   ├── execution_plan_template.md       # Phased agent execution plan template
│   └── verification_matrix_template.md  # Quality gate & test verification matrix
├── scripts/
│   ├── capability_checker.py            # CLI tool to inspect host environment & skills
│   └── prompt_optimizer_engine.py       # Algorithmic engine for classification & scoring
├── examples/
│   ├── 01_simple_prompt.md              # Level 0 (Simple code explanation)
│   ├── 02_coding_api.md                 # Level 2 (NestJS REST API creation)
│   ├── 03_existing_repo_refactor.md     # Level 2 (Repository architecture refactoring)
│   ├── 04_debugging_memory_leak.md      # Level 2 (Diagnosing and fixing memory leaks)
│   ├── 05_security_audit.md             # Level 3 (OWASP ASVS authentication audit)
│   ├── 06_complex_saas_architecture.md  # Level 4 (Multi-tenant B2B SaaS architecture)
│   ├── 07_research_rag_evaluation.md    # Level 4 (Comparative RAG architecture evaluation)
│   └── 08_multitool_issue_resolver.md   # Level 3 (Issue -> Code -> Test -> PR workflow)
└── tests/
    ├── __init__.py
    └── test_optimizer.py                # Automated Quality Gate verification suite
```

---

## Quick Start & Usage

### 1. Invocations

#### Command Line / Explicit
```text
/optimize-prompt Build a high-throughput webhook consumer in Go with Redis streams.
```

#### Contextual / Interactive
When invoked without arguments, the optimizer evaluates the current open files and conversation history:
```text
/optimize-prompt
```

### 2. Probing Environment Capabilities

Run the autonomous discovery prober to inspect what your current environment supports:
```bash
python scripts/capability_checker.py
```

### 3. Running the Quality Gate Test Suite

Validate all components, templates, references, and schemas:
```bash
python -m unittest tests/test_optimizer.py
```

---

## Output Modes

- **Mode A (Optimize Only)**: Returns capability analysis and the optimized prompt.
- **Mode B (Optimize + Prepare)**: Returns analysis, tool selections, the optimized prompt, phased execution plan, and verification matrix.
- **Mode C (Optimize + Execute)**: Fully automates the optimization, environment preparation, code execution, testing, and delivery reporting.

---

## License
MIT License. Free for open-source and enterprise agent engineering.
