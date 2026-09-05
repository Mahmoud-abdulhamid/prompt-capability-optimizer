# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Find-Skills Ecosystem Adapter
=============================
Real runtime integration for the open agent skills ecosystem (npx skills find).
Extracts verified packages, parses structured records, handles CLI failures gracefully,
and prevents automatic installation during discovery.
"""

import shutil
import subprocess
import json
import re
from typing import List, Dict, Any, Optional
from ..models import Resource, ResourceType, RiskLevel

class FindSkillsAdapter:
    
    TRUSTED_ORGS = {"vercel-labs", "anthropics", "google", "microsoft", "github", "composiohq"}
    
    def __init__(self):
        self.cli_available = shutil.which("npx") is not None
        self.version: Optional[str] = None
        self._query_cache: Dict[str, List[Resource]] = {}
        if self.cli_available:
            self._probe_version()
            
    def _probe_version(self):
        try:
            res = subprocess.run(
                ["npx", "--version"],
                capture_output=True,
                text=True,
                timeout=4
            )
            if res.returncode == 0:
                self.version = res.stdout.strip()
            else:
                self.cli_available = False
        except Exception:
            self.cli_available = False

    def search(self, query: str, limit: int = 5) -> List[Resource]:
        """
        Executes capability search against the open skills ecosystem.
        Handles missing CLI, timeouts, and network unavailability gracefully.
        """
        query_key = query.lower().strip()
        if not query_key:
            return []
            
        if query_key in self._query_cache:
            return self._query_cache[query_key][:limit]
            
        if not self.cli_available:
            return []
            
        results: List[Resource] = []
        try:
            # Execute skills find query without any install flags
            cmd = ["npx", "--yes", "skills", "find", query_key]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=8
            )
            if proc.returncode == 0 and proc.stdout:
                results = self._parse_skills_output(proc.stdout, query_key)
        except (subprocess.TimeoutExpired, FileNotFoundError, PermissionError, OSError):
            # Graceful fallback: return empty list without failing the entire optimization pipeline
            results = []
        except Exception:
            results = []
            
        self._query_cache[query_key] = results
        return results[:limit]

    def _parse_skills_output(self, output: str, query: str) -> List[Resource]:
        items: List[Resource] = []
        lines = output.splitlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("Browse") or "skills.sh" in line.lower():
                continue
                
            match = re.search(r"^([a-zA-Z0-9_\-\.\/]+)(?:\s*\(([\d\w\+]+)\s*installs?\))?(?:\s*[-–—:]\s*(.+))?$", line)
            if match:
                pkg_name = match.group(1).strip()
                installs_str = match.group(2) or "0"
                desc = match.group(3) or ""
                
                # Provenance and verified publisher check
                org = pkg_name.split("/")[0] if "/" in pkg_name else ""
                is_trusted_org = org.lower() in self.TRUSTED_ORGS
                
                # Parse install count metric for reputation
                installs = 0
                if "k" in installs_str.lower():
                    try:
                        installs = int(float(installs_str.lower().replace("k", "").replace("+", "")) * 1000)
                    except ValueError:
                        installs = 0
                else:
                    try:
                        installs = int(installs_str.replace("+", ""))
                    except ValueError:
                        installs = 0
                        
                reputation_score = min(10.0, 4.0 + (installs / 20000.0 * 5.0))
                trust_score = 9.0 if is_trusted_org else min(7.5, 4.0 + (installs / 50000.0 * 3.5))
                
                res = Resource(
                    id=f"find-skills:{pkg_name}",
                    name=pkg_name,
                    type=ResourceType.SKILL,
                    source="skills.sh",
                    capabilities=[query.lower(), f"skill-{org}" if org else "skill-community"],
                    location=f"https://skills.sh/{pkg_name}",
                    relevance=7.5,
                    capability_match=8.0,
                    quality=8.0 if len(desc) > 20 else 6.0,
                    trust=trust_score,
                    reputation=reputation_score,
                    compatibility=8.5,
                    freshness=8.0,
                    overhead=3.0,
                    risk=1.5 if is_trusted_org else 3.0,
                    risk_level=RiskLevel.EXTERNAL_SIDE_EFFECT,
                    permissions=["install_required"],
                    metadata={
                        "install_command": f"npx skills add {pkg_name}",
                        "installs": installs_str,
                        "description": desc,
                        "trusted_org": is_trusted_org,
                        "requires_approval": True
                    }
                )
                items.append(res)
        return items
