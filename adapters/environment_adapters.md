# Cross-Agent Environment Adapters & Fallback Hierarchy

This guide defines how `prompt-capability-optimizer` adapts to distinct host agent architectures without hardcoding dependencies or hallucinating capabilities.

---

## 1. Supported Agent Environments

| Agent System | Primary Skill Root | Tool Execution Mechanism | MCP Protocol | Web Capabilities |
| :--- | :--- | :--- | :--- | :--- |
| **Claude Code** | `~/.claude/skills`, `.claude/skills` | Native bash tool, view, edit | Yes (`mcp.json`) | Native search/fetch tools |
| **Gemini CLI / Antigravity** | `~/.gemini/config/skills`, `.gemini/skills` | Native `run_command`, `view_file`, `write_to_file` | Yes (`mcp_servers`, lazy/eager) | `search_web`, `read_url_content`, DevTools |
| **Cursor** | `.cursor/rules`, `.cursor/skills` | Built-in terminal, file edits | Experimental MCP | Integrated web search |
| **Windsurf** | `.codeium/windsurf/memories`, `.windsurf/` | Native file ops, terminal | MCP Client support | Integrated browser/search |
| **Cline / Roo Code** | `.cline/skills`, `.roo/skills` | Extension tools (execute_command, read_file) | Yes (full MCP config) | Native browser / Puppeteer |
| **OpenCode / Codex** | `.opencode/skills`, Project root | Shell execution, AST tools | Optional MCP | Curl / fetch fallback |

---

## 2. Dynamic Capability Abstraction Matrix

When constructing an optimized execution prompt, the optimizer queries the detected capabilities. If a preferred tool is absent, it seamlessly delegates to the designated fallback:

```text
[ Desired Task ] ─────────► [ Primary Native Tool ]
                                     │
                             (If unavailable)
                                     ▼
                            [ Fallback Level 1 ]
                                     │
                             (If unavailable)
                                     ▼
                            [ Fallback Level 2 ]
```

### Fallback Paths by Domain:

#### A. Web Search & Documentation Retrieval
1. **Primary**: Native Search Tool (`search_web`, `google_search`, or agent search tool).
2. **Fallback 1**: Web Fetch Tool (`read_url_content`, `curl`, `fetch`) targeting known official doc portals.
3. **Fallback 2**: Shell-based curl / Python script with JSON output:
   ```bash
   python -c "import urllib.request, json; print(urllib.request.urlopen('https://api.github.com/repos/...').read().decode('utf-8'))"
   ```
4. **Fallback 3**: Offline project inspection and local README/documentation analysis.

#### B. Skill Discovery & Management
1. **Primary**: Open Agent Skills CLI (`npx skills find`, `npx skills add`).
2. **Fallback 1**: Direct local filesystem scanning across multi-directory trees (`.gemini/skills`, `.claude/skills`, `~/.config/agent/skills`).
3. **Fallback 2**: Embedded reference patterns and inline specialized guidelines included directly inside the prompt.

#### C. Model Context Protocol (MCP)
1. **Primary**: Direct MCP Tool Call (`mcp_<server>_<tool>` or lazy loader `call_mcp_tool`).
2. **Fallback 1**: CLI wrapper / docker tool for the target service (e.g., `gh` CLI for GitHub, `psql` for PostgreSQL).
3. **Fallback 2**: REST API calls via Shell curl / HTTP libraries with environment credentials.
4. **Fallback 3**: Mock / local test doubles and synthetic data generation.

#### D. Subagent & Swarm Coordination
1. **Primary**: Native Agent Invocation (`invoke_subagent`, `teamwork-preview`).
2. **Fallback 1**: Sequential phased execution within the single agent context using checkpoints.
3. **Fallback 2**: Structured self-delegation prompts utilizing temporary branch workspaces.

---

## 3. Host Detection Algorithm

The optimizer runs an internal heuristic check to classify the host:

```python
def detect_host_runtime(env):
    if env.get("ANTIGRAVITY_AGENT") or "gemini" in env.get("PATH", "").lower():
        return "gemini_cli"
    elif env.get("CLAUDE_CODE_ENTRY") or ".claude" in env.get("CWD", ""):
        return "claude_code"
    elif env.get("CURSOR_PROJECT_DIR"):
        return "cursor"
    elif env.get("CLINE_ACTIVE"):
        return "cline"
    else:
        return "generic_agent"
```

---

## 4. Anti-Hallucination Invariant

> **Strict Rule**: The optimizer MUST NOT generate prompts requiring tools that the detected host agent cannot execute.

- If the host lacks MCP: The prompt must instruct the agent to use local CLI tools or REST scripts.
- If the host lacks internet access: The prompt must explicitly instruct the agent to operate exclusively on existing repository files and local standard libraries.
- If the host is Windows PowerShell: Commands must strictly avoid Unix-only constructs (e.g., avoid `export`, `cat file | grep`, prefer `Select-String`, `$env:VAR`).

---
**Author**: Mahmoud (<Develper.net@gmail.com>) | **Copyright**: © 2026 Mahmoud. All rights reserved. | **License**: MIT License
