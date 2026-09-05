"""
Host Runtime Abstraction
========================
Provides abstract interface for discovering capabilities, filesystem layouts,
and execution boundaries across different AI agent hosts.
"""

import os
import platform
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..models import HostCapabilityItem, CapabilityStatus

def detect_host_runtime() -> str:
    env = os.environ
    if env.get("ANTIGRAVITY_AGENT") or any("antigravity" in k.lower() for k in env):
        return "gemini_cli"
    if env.get("CLAUDE_CODE_ENTRY") or ".claude" in env.get("CWD", ""):
        return "claude_code"
    if env.get("CURSOR_PROJECT_DIR") or env.get("CURSOR_TRACE"):
        return "cursor"
    if env.get("CLINE_ACTIVE"):
        return "cline"
    if env.get("ROO_CODE"):
        return "roo_code"
    return "generic_agent"

class HostAdapter(ABC):
    
    @abstractmethod
    def get_agent_name(self) -> str:
        pass
        
    @abstractmethod
    def get_skill_paths(self) -> List[Path]:
        pass
        
    @abstractmethod
    def supports_mcp(self) -> HostCapabilityItem:
        pass
        
    @abstractmethod
    def supports_web(self) -> HostCapabilityItem:
        pass
