# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Unified Resource Registry
=========================
Maintains normalized inventory of all discoverable skills, tools, MCP servers,
and reference materials across the ecosystem.
"""

from typing import List, Dict, Optional, Set
from ..models import Resource, ResourceType, Capability

class ResourceRegistry:
    
    def __init__(self):
        self._resources: Dict[str, Resource] = {}
        
    def register(self, resource: Resource) -> None:
        self._resources[resource.id] = resource
        
    def register_many(self, resources: List[Resource]) -> None:
        for r in resources:
            self.register(r)
            
    def get(self, resource_id: str) -> Optional[Resource]:
        return self._resources.get(resource_id)
        
    def list_all(self) -> List[Resource]:
        return list(self._resources.values())
        
    def find_by_capability(self, capability_name: str) -> List[Resource]:
        matched = []
        c_lower = capability_name.lower().replace("-", " ")
        c_tokens = set(c_lower.split())
        
        for r in self._resources.values():
            # Check direct capability match
            direct_match = any(c_lower in cap.lower().replace("-", " ") for cap in r.capabilities)
            # Check name match
            name_tokens = set(r.name.lower().replace("-", " ").replace("_", " ").split())
            token_overlap = len(c_tokens.intersection(name_tokens))
            
            if direct_match or token_overlap > 0:
                # Dynamically calculate match score based on token relevance
                r.capability_match = 9.0 if direct_match else min(8.0, 5.0 + (token_overlap * 1.5))
                matched.append(r)
                
        return matched
        
    def clear(self) -> None:
        self._resources.clear()
