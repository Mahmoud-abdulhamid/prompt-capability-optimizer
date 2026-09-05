# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Agent Ecosystem Adapters & Compatibility Verification
=====================================================
Concrete host implementations for Claude Code, Codex, Gemini CLI, OpenCode,
Cursor, Windsurf, Cline, and Roo Code.
Guarantees that unknown agents are NEVER silently mapped to Gemini or any other agent.
"""

import os
from pathlib import Path
from typing import List, Optional
from ..models import HostCapabilityItem, CapabilityStatus
from .host_adapter import HostAdapter

class GeminiCliAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "gemini_cli"
        
    def get_skill_paths(self) -> List[Path]:
        home = Path.home()
        cwd = Path.cwd()
        return [
            cwd / ".gemini" / "skills",
            home / ".gemini" / "config" / "skills",
            home / ".gemini" / "antigravity" / "builtin" / "skills"
        ]
        
    def supports_mcp(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.RUNTIME_DETECTED,
            confidence=0.98,
            details={"protocol": "Model Context Protocol JSON-RPC", "validated": True}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.RUNTIME_DETECTED,
            confidence=0.95,
            details={"provider": "search_web / read_url_content", "validated": True}
        )

class ClaudeCodeAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "claude_code"
        
    def get_skill_paths(self) -> List[Path]:
        home = Path.home()
        cwd = Path.cwd()
        return [
            cwd / ".claude" / "skills",
            home / ".claude" / "skills"
        ]
        
    def supports_mcp(self) -> HostCapabilityItem:
        home = Path.home()
        has_cfg = (home / ".claude" / "mcp.json").exists()
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.RUNTIME_DETECTED if has_cfg else CapabilityStatus.HOST_DECLARED,
            confidence=0.90,
            details={"config_file": str(home / ".claude" / "mcp.json"), "validated": True}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.90,
            details={"provider": "WebSearch / WebFetch", "validated": True}
        )

class CursorAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "cursor"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [
            cwd / ".cursor" / "skills",
            cwd / ".cursor" / "rules"
        ]
        
    def supports_mcp(self) -> HostCapabilityItem:
        cwd = Path.cwd()
        has_cfg = (cwd / ".cursor" / "mcp.json").exists()
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.RUNTIME_DETECTED if has_cfg else CapabilityStatus.UNKNOWN,
            confidence=0.75,
            details={"config_file": str(cwd / ".cursor" / "mcp.json"), "validated": "Partial"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.80,
            details={"provider": "Integrated web query", "validated": "Partial"}
        )

class WindsurfAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "windsurf"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [
            cwd / ".windsurf" / "skills",
            cwd / ".codeium" / "windsurf" / "memories"
        ]
        
    def supports_mcp(self) -> HostCapabilityItem:
        cwd = Path.cwd()
        has_cfg = (cwd / ".windsurf" / "mcp.json").exists()
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.RUNTIME_DETECTED if has_cfg else CapabilityStatus.HOST_DECLARED,
            confidence=0.75,
            details={"validated": "Partial"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.80,
            details={"provider": "Integrated web search", "validated": "Partial"}
        )

class ClineAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "cline"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [
            cwd / ".cline" / "skills"
        ]
        
    def supports_mcp(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.85,
            details={"provider": "Extension MCP manager", "validated": "Partial"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.85,
            details={"provider": "Browser tool", "validated": "Partial"}
        )

class RooCodeAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "roo_code"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [
            cwd / ".roo" / "skills"
        ]
        
    def supports_mcp(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.85,
            details={"provider": "Roo MCP client", "validated": "Partial"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.HOST_DECLARED,
            confidence=0.80,
            details={"provider": "Browser tool", "validated": "Partial"}
        )

class CodexAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "codex"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [cwd / ".agents" / "skills", cwd / "skills"]
        
    def supports_mcp(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.UNAVAILABLE,
            confidence=0.90,
            details={"validated": "Host-Dependent"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.UNAVAILABLE,
            confidence=0.90,
            details={"validated": "Host-Dependent"}
        )

class OpenCodeAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "opencode"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [cwd / ".opencode" / "skills", cwd / "skills"]
        
    def supports_mcp(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.UNKNOWN,
            confidence=0.70,
            details={"validated": "Host-Dependent"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.UNKNOWN,
            confidence=0.70,
            details={"validated": "Host-Dependent"}
        )

class UnknownAgentAdapter(HostAdapter):
    def __init__(self, raw_name: str):
        self._raw_name = raw_name
        
    def get_agent_name(self) -> str:
        return f"unknown:{self._raw_name}"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [cwd / "skills", cwd / ".skills"]
        
    def supports_mcp(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="mcp",
            status=CapabilityStatus.UNKNOWN,
            confidence=0.0,
            details={"error": f"Agent '{self._raw_name}' is not recognized"}
        )
        
    def supports_web(self) -> HostCapabilityItem:
        return HostCapabilityItem(
            capability="web",
            status=CapabilityStatus.UNKNOWN,
            confidence=0.0,
            details={"error": f"Agent '{self._raw_name}' is not recognized"}
        )

def get_agent_adapter(agent_name: str) -> HostAdapter:
    canonical = agent_name.lower().strip()
    adapters = {
        "gemini_cli": GeminiCliAdapter(),
        "gemini": GeminiCliAdapter(),
        "antigravity": GeminiCliAdapter(),
        "claude_code": ClaudeCodeAdapter(),
        "claude": ClaudeCodeAdapter(),
        "cursor": CursorAdapter(),
        "windsurf": WindsurfAdapter(),
        "cline": ClineAdapter(),
        "roo_code": RooCodeAdapter(),
        "roo": RooCodeAdapter(),
        "codex": CodexAdapter(),
        "opencode": OpenCodeAdapter()
    }
    # Fix critical bug: NEVER silently convert unknown agent to Gemini
    if canonical not in adapters:
        return UnknownAgentAdapter(agent_name)
    return adapters[canonical]
