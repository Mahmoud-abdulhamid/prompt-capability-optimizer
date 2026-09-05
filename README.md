# Prompt Capability Optimizer (`prompt-capability-optimizer`)

[![npm version](https://img.shields.io/npm/v/prompt-capability-optimizer.svg)](https://www.npmjs.com/package/prompt-capability-optimizer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Production-Grade, Cross-Platform Agent Meta-Skill for Autonomous Capability Discovery & Two-Pass Prompt Optimization**  
> **Author & Architect**: **Mahmoud Abdelhameid** ([LinkedIn](https://www.linkedin.com/in/mahmoud-abdelhameid-dev/) | [Email](mailto:Develper.net@gmail.com)) | **License**: MIT | **Version**: 1.0.0

`prompt-capability-optimizer` sits between a user's raw prompt and an AI coding agent's execution loop. It combines the active discovery principles of `find-skills` with professional prompt-engineering standards to generate mathematically sound, tool-aware, verified, and secure prompts without expanding verbosity.

---

## 1. What It Does

1. **Classifies Task Depth**: Adaptively categorizes requests from Level 0 (Simple/Informational) to Level 4 (Enterprise Multi-System SaaS).
2. **Discovers Real Capabilities**: Scans local file paths, host-declared MCP servers, the open `skills.sh` registry, and authoritative web documentation.
3. **Applies Strict Security Gates**: Enforces the "Never Install Blindly" governance protocol, redacts secrets (API keys, JWTs, DB URLs), and neutralizes adversarial prompt injection payloads.
4. **Calculates Normalized Utility**: Uses a single deterministic scoring formula from `references/scoring_rubric.md` and eliminates duplicate tools.
5. **Executes Two-Pass Optimization**:
   - **Pass 1 (Semantic)**: Clarifies objectives, contracts, and negative constraints while preserving 100% of user intent.
   - **Pass 2 (Execution)**: Binds real tools, phased execution milestones, and repository-derived verification commands.
6. **Runs Real Self-Critique**: Tests candidate prompts against a 13-point rubric; automatically executes a correction pass if requirements are missing.

---

## 2. Cross-Agent Support Matrix

| Agent Host | Runtime Status | Skill Discovery | MCP Discovery | Web Guidance | Fallback Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Gemini CLI / Antigravity** | **Validated** | `~/.gemini/config/skills` | `~/.gemini/antigravity/mcp` | Native search & fetch | Full native support |
| **Claude Code** | **Validated** | `~/.claude/skills` | `~/.claude/mcp.json` | WebSearch / WebFetch | Full native support |
| **Cline / Roo Code** | **Validated** | `.cline/skills`, `.roo/skills` | Extension MCP | Extension browser | Host declared |
| **Cursor** | **Partial** | `.cursor/rules`, `.cursor/skills` | `.cursor/mcp.json` | Integrated search | Graceful CLI fallback |
| **Windsurf** | **Partial** | `.windsurf/` | Native MCP config | Integrated search | Graceful CLI fallback |
| **Codex / OpenCode** | **Host-Dependent** | Repository root / skills | Custom CLI / JSON-RPC | Shell curl / python | Generic fallback |

---

## 3. Architecture Pipeline

```text
                         RAW USER PROMPT
                               │
                               ▼
                      ┌─────────────────┐
                      │ Intent Analyzer │
                      └────────┬────────┘
                               ▼
                     ┌───────────────────┐
                     │  Task Classifier  │ (Level 0 - 4)
                     └────────┬──────────┘
                              ▼
                   ┌──────────────────────┐
                   │ Capability Extractor │
                   └──────────┬───────────┘
                              ▼
                 ┌──────────────────────────┐
                 │ Host Capability Adapter  │
                 └────────────┬─────────────┘
                              ▼
        ┌──────────────────────────────────────────┐
        │          Capability Discovery            │
        │                                          │
        │ Local Skills   find-skills   MCP         │
        │ Connectors     Plugins       Web         │
        │ Built-in Tools              Docs         │
        └─────────────────────┬────────────────────┘
                              ▼
                     ┌─────────────────┐
                     │  Trust Engine   │ (Reputation vs. Trust)
                     └────────┬────────┘
                              ▼
                     ┌─────────────────┐
                     │ Scoring Engine  │ (Authoritative Utility Formula)
                     └────────┬────────┘
                              ▼
                    ┌───────────────────┐
                    │  Deduplication    │ (Context Budgeting)
                    └─────────┬─────────┘
                              ▼
                  ┌───────────────────────┐
                  │ Semantic Pass (Pass 1)│
                  └───────────┬───────────┘
                              ▼
                  ┌───────────────────────┐
                  │Execution Pass (Pass 2)│
                  └───────────┬───────────┘
                              ▼
                     ┌─────────────────┐
                     │  Self-Critique  │
                     └────────┬────────┘
                              │
                       FAIL ──┘
                              │
                              ▼
                       Correction Pass
                              │
                              ▼
                     ┌─────────────────┐
                     │  Verification   │ (Repository-aware: package.json / pytest)
                     └────────┬────────┘
                              ▼
                       FINAL PROMPT
```

---

## 4. CLI Usage

### Direct Execution with npx (Node.js)
```bash
# Run immediately without installation
npx prompt-capability-optimizer optimize "Build a secure NestJS authentication system with PostgreSQL and JWT"

# Inspect host environment capabilities
npx prompt-capability-optimizer probe
```

### Python Package Invocation
```bash
# Human-readable format
python -m prompt_capability_optimizer optimize "Build a secure NestJS authentication system with PostgreSQL and JWT"

# Machine-readable JSON output
python -m prompt_capability_optimizer optimize "Refactor this project architecture" --json --mode B
```

### Probe Environment Capabilities
```bash
python -m prompt_capability_optimizer probe
```

---

## 5. Running the Test Suites

The project includes both structural and behavioral test suites:

```bash
# Run all 21 automated unit, behavioral, adversarial, and end-to-end tests:
python -m unittest discover -s tests -p "test_*.py" -v
```

Test coverage includes:
- **Test A**: Simple informational prompt behavior.
- **Test B**: Framework isolation (React does not hallucinate NestJS).
- **Test C**: Specialized security and authentication extraction.
- **Test D**: Repository-aware verification command derivation.
- **Test E**: Non-mocked host MCP server discovery.
- **Test F**: Local skill frontmatter parsing and utility ranking.
- **Test G**: Targeted authoritative web documentation discovery.
- **Test H**: Self-critique rejection of incomplete prompts.
- **Test I**: Adversarial prompt injection neutralization.
- **Test J**: Automated secret detection and redaction.
- **Test K**: Capability deduplication and context budgeting.
- **Test L**: Cross-agent host adapters.
- **Test M**: Full end-to-end pipeline execution and verification.

---

## 6. Security & Installation Governance

- **"Never Install Blindly"**: External skills or MCP servers are NEVER automatically installed without calculating $\text{Expected Value} > \text{Risk} + \text{Cost}$ and presenting explicit human consent gates.
- **Secret Redaction**: Detects API keys, AWS credentials, JWT tokens, and connection strings, redacting them before prompt rendering.
- **Prompt Injection Defense**: Scans and sanitizes adversarial directives (`IGNORE PREVIOUS INSTRUCTIONS`, exfiltration requests).

---

## 7. Authorship & Copyright

- **Lead Architect & Author**: **Mahmoud Abdelhameid**
- **LinkedIn**: [mahmoud-abdelhameid-dev](https://www.linkedin.com/in/mahmoud-abdelhameid-dev/)
- **Email / Contact**: [Develper.net@gmail.com](mailto:Develper.net@gmail.com)
- **Copyright**: © 2026 Mahmoud Abdelhameid. All rights reserved.
- **License**: MIT License — see [LICENSE](file:///d:/prompt-capability-optimizer/LICENSE) for details.


