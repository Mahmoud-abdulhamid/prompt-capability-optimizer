# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

#!/usr/bin/env python3
"""
Host Runtime Capability & Skill Prober
======================================
Autonomous discovery tool for prompt-capability-optimizer.
Inspects local filesystem, active agent environment variables, and skill roots
to construct a deterministic Host Capability Report using the core engine.
"""

import sys
import json
import shutil
import platform
from pathlib import Path

# Add parent directory to sys.path so it can import the package
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from prompt_capability_optimizer.adapters.host_adapter import detect_host_runtime
from prompt_capability_optimizer.discovery.local_discovery import LocalSkillDiscovery
from prompt_capability_optimizer.discovery.mcp_discovery import McpDiscovery
from prompt_capability_optimizer.models import CapabilityStatus

def probe_installed_tooling():
    binaries = [
        "git", "node", "npm", "npx", "python", "python3", "docker",
        "gh", "cargo", "go", "tsc", "pytest", "ruff", "eslint"
    ]
    return {b: shutil.which(b) is not None for b in binaries}

def generate_report():
    current_os = platform.system().lower()
    shell = "powershell" if current_os == "windows" else "bash"
    agent_identity = detect_host_runtime()
    
    # Real local discovery without mocks
    skills = LocalSkillDiscovery.discover()
    mcp_resources = McpDiscovery.discover()
    tooling = probe_installed_tooling()
    
    # Map real MCP server statuses
    active_mcp_names = [m.name for m in mcp_resources]
    
    report = {
        "agent_identity": agent_identity,
        "runtime_environment": {
            "os": current_os,
            "shell_type": shell,
            "working_directory": str(Path.cwd().resolve())
        },
        "capabilities": {
            "supports_filesystem": {"available": True, "methods": ["native_tool", "full_access"]},
            "supports_shell": {"available": True, "supports_async": True, "interactive_input": True},
            "supports_git": {"available": tooling.get("git", False), "in_git_repo": (Path.cwd() / ".git").exists()},
            "supports_web_search": {"available": True, "provider": "native"},
            "supports_web_fetch": {"available": True, "javascript_execution": False},
            "supports_mcp": {
                "available": len(active_mcp_names) > 0,
                "status": "runtime_detected" if len(active_mcp_names) > 0 else "unknown",
                "active_servers": active_mcp_names
            },
            "supports_skills": {
                "available": True,
                "discovered_count": len(skills),
                "skills": [
                    {"name": s.name, "path": s.location, "scope": s.metadata.get("scope", "user")}
                    for s in skills
                ],
                "registry_cli_available": tooling.get("npx", False)
            },
            "installed_tooling": tooling
        }
    }
    return report

if __name__ == "__main__":
    rep = generate_report()
    if "--json" in sys.argv or len(sys.argv) == 1:
        print(json.dumps(rep, indent=2))
    else:
        print(f"Agent Identity: {rep['agent_identity']}")
        print(f"OS: {rep['runtime_environment']['os']} ({rep['runtime_environment']['shell_type']})")
        print(f"Discovered Skills: {len(rep['capabilities']['supports_skills']['skills'])}")
        print(f"Active MCP Servers: {', '.join(rep['capabilities']['supports_mcp']['active_servers'])}")
