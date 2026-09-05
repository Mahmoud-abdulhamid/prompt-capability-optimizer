"""
Real Model Context Protocol (MCP) Discovery
===========================================
Inspects host configuration paths and agent metadata to discover actually available
MCP servers, tools, and schemas without hardcoded assumptions.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..models import Resource, ResourceType, RiskLevel

class McpDiscovery:
    
    @classmethod
    def discover(cls) -> List[Resource]:
        home = Path.home()
        cwd = Path.cwd()
        
        discovered_servers: List[Resource] = []
        seen_server_names = set()
        
        # 1. Inspect Antigravity / Gemini MCP directory: ~/.gemini/antigravity/mcp/<server_name>
        agy_mcp_dir = home / ".gemini" / "antigravity" / "mcp"
        if agy_mcp_dir.exists() and agy_mcp_dir.is_dir():
            try:
                for server_folder in agy_mcp_dir.iterdir():
                    if server_folder.is_dir():
                        s_name = server_folder.name
                        if s_name in seen_server_names:
                            continue
                        seen_server_names.add(s_name)
                        
                        # Collect tool schemas inside this MCP server folder
                        tools = [f.stem for f in server_folder.glob("*.json")]
                        
                        res = Resource(
                            id=f"mcp:{s_name}",
                            name=s_name,
                            type=ResourceType.MCP,
                            source="host_mcp_dir",
                            capabilities=[f"mcp-{s_name}"] + tools,
                            location=str(server_folder.resolve()),
                            relevance=7.0,
                            capability_match=8.0,
                            quality=9.0,
                            trust=9.0,
                            reputation=8.5,
                            compatibility=10.0,
                            freshness=9.0,
                            overhead=2.0,
                            risk=1.0,
                            risk_level=RiskLevel.LOW_RISK,
                            permissions=["mcp_tool_invocation"],
                            metadata={
                                "server_name": s_name,
                                "tools": tools,
                                "status": "runtime_detected"
                            }
                        )
                        discovered_servers.append(res)
            except Exception:
                pass
                
        # 2. Inspect Claude / Cursor / VSCode mcp.json configs
        config_candidates = [
            cwd / ".cursor" / "mcp.json",
            cwd / ".vscode" / "mcp.json",
            home / ".claude" / "mcp.json"
        ]
        for cfg in config_candidates:
            if cfg.exists() and cfg.is_file():
                try:
                    data = json.loads(cfg.read_text(encoding="utf-8", errors="replace"))
                    servers = data.get("mcpServers", {})
                    for s_name, s_conf in servers.items():
                        if s_name in seen_server_names:
                            continue
                        seen_server_names.add(s_name)
                        
                        res = Resource(
                            id=f"mcp:{s_name}",
                            name=s_name,
                            type=ResourceType.MCP,
                            source=f"config:{cfg.name}",
                            capabilities=[f"mcp-{s_name}"],
                            location=str(cfg.resolve()),
                            relevance=7.0,
                            capability_match=7.5,
                            quality=8.5,
                            trust=8.5,
                            reputation=8.0,
                            compatibility=9.0,
                            freshness=8.5,
                            overhead=2.5,
                            risk=1.5,
                            risk_level=RiskLevel.LOW_RISK,
                            permissions=["mcp_tool_invocation"],
                            metadata={
                                "server_name": s_name,
                                "command": s_conf.get("command"),
                                "status": "host_declared"
                            }
                        )
                        discovered_servers.append(res)
                except Exception:
                    continue
                    
        return discovered_servers
