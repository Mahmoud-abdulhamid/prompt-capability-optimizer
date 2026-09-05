# Cross-Agent Capability Matrix & Command Rosetta Stone

This reference maps common agent intents and commands across primary AI agent ecosystems, providing standard equivalents and fallback paths.

---

## 1. Unified Command Rosetta Stone

| Intent / Operation | Claude Code | Gemini CLI / Antigravity | Cursor / Windsurf | Cline / Roo Code | Generic Agent |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Inspect File** | `View` | `view_file` | Editor API / `read_file` | `read_file` | `cat` / `type` / python script |
| **Edit File** | `Edit` / `Replace` | `replace_file_content` | Inline Editor / Linter | `replace_in_file` | `sed` / python script / patch |
| **Create File** | `Write` | `write_to_file` | Editor API / `new_file` | `write_to_file` | `Set-Content` / `tee` |
| **Execute Command** | `Bash` | `run_command` | Integrated Terminal | `execute_command` | Subprocess shell |
| **Web Search** | `WebSearch` | `search_web` | Built-in web query | `browser_action` | HTTP API / curl |
| **Read Web Page** | `WebFetch` | `read_url_content` | Built-in scraper | `fetch` / Puppeteer | Python `urllib` / `curl` |
| **Invoke Subagent** | Native dispatch | `invoke_subagent` | N/A (single loop) | Task manager | Process fork / subshell |
| **MCP Interaction** | Built-in MCP | `call_mcp_tool` | MCP client | `use_mcp_tool` | JSON-RPC 2.0 pipe |

---

## 2. Directory Resolution Mapping

When scanning for local skills across environments:

```text
Host Environment      Path Checked
─────────────────────────────────────────────────────────────────────────────
All / Standard:       ./skills/
                      ./.skills/
                      ~/.config/agent/skills/

Claude Code:          ./.claude/skills/
                      ~/.claude/skills/

Gemini / Antigravity: ./.gemini/skills/
                      ~/.gemini/config/skills/
                      ~/.gemini/antigravity/builtin/skills/

Cursor / Windsurf:    ./.cursor/skills/
                      ./.cursor/rules/
                      ./.windsurf/skills/

Cline / Roo Code:     ./.cline/skills/
                      ./.roo/skills/
```

---

## 3. Graceful Fallback Strategy

When a prompt is generated for an environment lacking a specific capability:

1. **Subagent Delegation Missing**:
   - The prompt specifies a **Step-by-Step Self-Review Phase**, where the single agent pauses, checks its own work against the verification matrix, and records findings before continuing.
2. **Web Browsing Missing**:
   - The prompt directs the agent to utilize standard library documentation, installed package types (`node_modules/@types`, python docstrings), or local test suites.
3. **MCP Missing**:
   - The prompt provides direct CLI commands or standard REST/cURL commands utilizing existing system binaries (e.g., using `gh` CLI instead of GitHub MCP).
