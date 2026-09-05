# Capability Scoring Rubric & Redundancy Elimination

This reference defines the deterministic scoring model used by `prompt-capability-optimizer` to evaluate, rank, and select candidate skills, MCP servers, and tools.

---

## 1. Multi-Factor Scoring Formula

Every discovered capability $c$ is assigned an individual attribute score from $0.0$ to $10.0$ across 8 dimensions:

| Dimension | Weight ($w_i$) | Description |
| :--- | :--- | :--- |
| **Relevance** ($R$) | 0.25 | Directness of alignment with primary task intent. |
| **Capability Match** ($M$) | 0.25 | How comprehensively the tool solves the required technical node. |
| **Code / Skill Quality** ($Q$) | 0.15 | Structure, completeness of examples, clear error handling, documentation. |
| **Trust & Provenance** ($T$) | 0.15 | Official org author (10), verified ecosystem author (8), unknown author (2). |
| **Compatibility** ($C$) | 0.10 | Runtime and platform match (OS, language version, package compatibility). |
| **Freshness** ($F$) | 0.05 | Recent maintenance, up-to-date with current language specifications. |
| **Overhead & Complexity** ($O$) | -0.10 | Context consumption, setup friction, latency impact. |
| **Security Risk** ($K$) | -0.20 | Dangerous privileges, credential exposure, untrusted binaries. |

### Composite Utility Score:
$$\text{Utility}(c) = (0.25 R + 0.25 M + 0.15 Q + 0.15 T + 0.10 C + 0.05 F) - (0.10 O + 0.20 K)$$

---

## 2. Selection Thresholds

- **Utility $\ge 7.0$**: **Auto-Adopt**. Capability is immediately selected and woven into the prompt.
- **$5.0 \le \text{Utility} < 7.0$**: **Conditional Recommendation**. Included only if no higher-scoring alternative covers that capability node.
- **Utility $< 5.0$**: **Reject**. Do not burden agent context with marginal or risky tools.

---

## 3. Redundancy Elimination & Deduplication Protocol

When multiple candidate skills or tools compete for the same capability node:

1. **Exact Domain Overlap**:
   - *Example*: Both `nestjs-auth-jwt` and `general-jwt-generator` are available.
   - *Rule*: Prefer the more domain-specialized skill (`nestjs-auth-jwt`) if its Trust $\ge 7.0$.
2. **Context Budget Enforcement**:
   - Limit total active skills in a single prompt to a maximum of **3** (or **5** for Level 4 tasks).
   - Never activate two skills that instruct the agent on the same underlying abstraction (e.g., two different ORM guides).
3. **Hierarchy of Provenance**:
   $$\text{Official Maintainer} > \text{Verified Community} > \text{Generic Community} > \text{Ad-hoc Web Snippet}$$

---
**Author**: Mahmoud Abdelhameid ([LinkedIn](https://www.linkedin.com/in/mahmoud-abdelhameid-dev/) | [Email](mailto:Develper.net@gmail.com)) | **Copyright**: © 2026 Mahmoud Abdelhameid. All rights reserved. | **License**: MIT License
