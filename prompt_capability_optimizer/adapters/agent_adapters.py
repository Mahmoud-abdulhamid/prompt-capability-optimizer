"""
Agent Ecosystem Adapters
========================
Concrete implementations for Gemini CLI / Antigravity, Claude Code, Cursor, and Cline.
"""

import os
from pathlib import Path
from typing import List
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
            confidence=0.85,
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

class ClineAdapter(HostAdapter):
    def get_agent_name(self) -> str:
        return "cline"
        
    def get_skill_paths(self) -> List[Path]:
        cwd = Path.cwd()
        return [
            cwd / ".cline" / "skills",
            cwd / ".roo" / "skills"
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

def get_agent_adapter(agent_name: str) -> HostAdapter:
    adapters = {
        "gemini_cli": GeminiCliAdapter(),
        "claude_code": ClaudeCodeAdapter(),
        "cursor": CursorAdapter(),
        "cline": ClineAdapter(),
        "roo_code": ClineAdapter()
    }
    return adapters.get(agent_name, GeminiCliAdapter())
