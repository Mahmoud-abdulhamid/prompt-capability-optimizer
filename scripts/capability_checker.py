#!/usr/bin/env python3
"""
Host Runtime Capability & Skill Prober
======================================
Autonomous discovery tool for prompt-capability-optimizer.
Inspects local filesystem, active agent environment variables, and skill roots
to construct a deterministic Host Capability Report.
"""

import os
import sys
import json
import shutil
import platform
from pathlib import Path

def detect_os_and_shell():
    current_os = platform.system().lower()
    if current_os == "windows":
        os_type = "windows"
        shell = "powershell" if os.environ.get("PSModulePath") else "cmd"
    elif current_os == "darwin":
        os_type = "darwin"
        shell = os.environ.get("SHELL", "zsh").split("/")[-1]
    else:
        os_type = "linux"
        shell = os.environ.get("SHELL", "bash").split("/")[-1]
    return os_type, shell

def detect_agent_runtime():
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

def scan_local_skills():
    home = Path.home()
    cwd = Path.cwd()
    
    candidate_paths = [
        cwd / ".gemini" / "skills",
        cwd / ".claude" / "skills",
        cwd / ".cursor" / "skills",
        cwd / ".cline" / "skills",
        cwd / "skills",
        cwd / ".skills",
        home / ".gemini" / "config" / "skills",
        home / ".gemini" / "antigravity" / "builtin" / "skills",
        home / ".claude" / "skills",
        home / ".config" / "agent" / "skills"
    ]
    
    discovered_skills = []
    seen = set()
    
    for base_path in candidate_paths:
        if base_path.exists() and base_path.is_dir():
            for item in base_path.iterdir():
                if item.is_dir():
                    skill_file = item / "SKILL.md"
                    if skill_file.exists():
                        name = item.name
                        if name not in seen:
                            seen.add(name)
                            discovered_skills.append({
                                "name": name,
                                "path": str(skill_file.resolve()),
                                "scope": "project" if cwd in skill_file.parents else "user"
                            })
    return discovered_skills

def probe_installed_tooling():
    binaries = [
        "git", "node", "npm", "npx", "python", "python3", "docker",
        "gh", "cargo", "go", "tsc", "pytest", "ruff", "eslint"
    ]
    installed = {}
    for b in binaries:
        installed[b] = shutil.which(b) is not None
    return installed

def generate_report():
    os_type, shell = detect_os_and_shell()
    agent_identity = detect_agent_runtime()
    skills = scan_local_skills()
    tooling = probe_installed_tooling()
    
    report = {
        "agent_identity": agent_identity,
        "runtime_environment": {
            "os": os_type,
            "shell_type": shell,
            "working_directory": str(Path.cwd().resolve())
        },
        "capabilities": {
            "supports_filesystem": {"available": True, "methods": ["native_tool", "full_access"]},
            "supports_shell": {"available": True, "supports_async": True, "interactive_input": True},
            "supports_git": {"available": tooling.get("git", False), "in_git_repo": (Path.cwd() / ".git").exists()},
            "supports_web_search": {"available": True, "provider": "native"},
            "supports_web_fetch": {"available": True, "javascript_execution": False},
            "supports_mcp": {"available": True, "active_servers": ["supabase", "gemini-api-docs", "chrome-devtools-mcp"]},
            "supports_skills": {
                "available": True,
                "discovered_count": len(skills),
                "skills": skills,
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
        for s in rep['capabilities']['supports_skills']['skills']:
            print(f"  - {s['name']} ({s['scope']})")
