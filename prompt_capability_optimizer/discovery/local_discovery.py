# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Real Local Skill Discovery
==========================
Inspects filesystem paths across project and user roots, parses SKILL.md frontmatter,
and creates normalized Resource instances.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..models import Resource, ResourceType, RiskLevel

class LocalSkillDiscovery:
    
    @staticmethod
    def parse_skill_frontmatter(file_path: Path) -> Dict[str, str]:
        metadata = {"name": file_path.parent.name, "description": ""}
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
            # Parse YAML frontmatter between --- and ---
            match = re.search(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if match:
                yaml_text = match.group(1)
                for line in yaml_text.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        metadata[k.strip().lower()] = v.strip().strip("'\"")
            else:
                # Fallback to first heading
                h1 = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if h1:
                    metadata["name"] = h1.group(1).strip()
        except Exception:
            pass
        return metadata

    @classmethod
    def discover(cls, custom_roots: Optional[List[Path]] = None) -> List[Resource]:
        home = Path.home()
        cwd = Path.cwd()
        
        search_roots = custom_roots or [
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
        
        discovered: List[Resource] = []
        seen_names = set()
        
        for base in search_roots:
            if not base.exists() or not base.is_dir():
                continue
                
            try:
                for item in base.iterdir():
                    if item.is_dir():
                        skill_file = item / "SKILL.md"
                        if skill_file.exists():
                            meta = cls.parse_skill_frontmatter(skill_file)
                            name = meta.get("name", item.name)
                            if name in seen_names:
                                continue
                            seen_names.add(name)
                            
                            is_builtin = "builtin" in str(base).lower()
                            is_user = home in skill_file.parents
                            scope = "builtin" if is_builtin else ("user" if is_user else "project")
                            trust_score = 9.5 if is_builtin else (8.5 if not is_user else 8.0)
                            
                            desc = meta.get("description", "")
                            # Derive capabilities from name and description
                            tokens = set(re.findall(r"[A-Za-z0-9_\-]+", f"{name} {desc}".lower()))
                            
                            resource = Resource(
                                id=f"skill:{name}",
                                name=name,
                                type=ResourceType.SKILL,
                                source=f"local_{scope}",
                                capabilities=list(tokens),
                                location=str(skill_file.resolve()),
                                relevance=6.0,
                                capability_match=6.0,
                                quality=8.5 if len(desc) > 30 else 6.0,
                                trust=trust_score,
                                reputation=8.0,
                                compatibility=9.5,
                                freshness=8.0,
                                overhead=1.5,
                                risk=0.5,
                                risk_level=RiskLevel.NO_SIDE_EFFECT,
                                permissions=["read_only"],
                                metadata={
                                    "description": desc,
                                    "scope": scope,
                                    "file_path": str(skill_file)
                                }
                            )
                            discovered.append(resource)
            except Exception:
                continue
                
        return discovered
