"""
Unified Command Line Interface
==============================
Provides standard CLI commands for prompt optimization and environment probing.
Usage:
  python -m prompt_capability_optimizer optimize "Build a NestJS auth API" --json
  python -m prompt_capability_optimizer probe
"""

import sys
import json
import argparse
from .engine import PromptOptimizerEngine
from .discovery.local_discovery import LocalSkillDiscovery
from .discovery.mcp_discovery import McpDiscovery
from .adapters.host_adapter import detect_host_runtime

def main():
    parser = argparse.ArgumentParser(
        prog="prompt-capability-optimizer",
        description="Autonomous Capability Discovery & Two-Pass Prompt Engineering Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")
    
    # optimize subcommand
    opt_parser = subparsers.add_parser("optimize", help="Optimize a raw prompt")
    opt_parser.add_argument("prompt", type=str, help="The prompt text to optimize")
    opt_parser.add_argument("--mode", type=str, choices=["A", "B", "C"], default="B", help="Output mode (A: optimize only, B: prepare, C: execute)")
    opt_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    
    # probe subcommand
    probe_parser = subparsers.add_parser("probe", help="Probe host capabilities and discovered skills")
    probe_parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()
    
    if args.command == "optimize":
        engine = PromptOptimizerEngine()
        result = engine.optimize(args.prompt, mode=args.mode)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"=== Prompt Capability Optimizer (Mode {result['mode']}) ===")
            print(f"Classification Level: {result['classification']['level']} ({result['classification']['reasoning']})")
            print(f"Discovered Capabilities: {', '.join(result['required_capabilities'])}")
            print(f"Critique Pass: {result['critique']['passed']} (Score: {result['critique']['score']})\n")
            print("--- OPTIMIZED PROMPT ---")
            print(result["optimized_prompt"])
            
    elif args.command == "probe":
        host_agent = detect_host_runtime()
        skills = LocalSkillDiscovery.discover()
        mcp_servers = McpDiscovery.discover()
        
        rep = {
            "host_agent": host_agent,
            "local_skills_count": len(skills),
            "local_skills": [{"name": s.name, "source": s.source} for s in skills],
            "mcp_servers_count": len(mcp_servers),
            "mcp_servers": [{"name": m.name, "tools": m.metadata.get("tools", [])} for m in mcp_servers]
        }
        
        if args.json or True:
            print(json.dumps(rep, indent=2))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
