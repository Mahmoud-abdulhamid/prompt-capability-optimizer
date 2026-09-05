"""
Capability Graph & Dependency Resolver
======================================
Builds dependency trees from required capabilities and resolves prerequisite nodes.
"""

from typing import List, Dict, Set, Any
from ..models import Capability

class CapabilityGraph:
    
    def __init__(self, roots: List[Capability]):
        self.nodes: Dict[str, Capability] = {c.name: c for c in roots}
        self._expand_dependencies()
        
    def _expand_dependencies(self):
        to_process = list(self.nodes.values())
        while to_process:
            current = to_process.pop(0)
            for dep_name in current.dependencies:
                if dep_name not in self.nodes:
                    new_node = Capability(
                        name=dep_name,
                        domain=current.domain,
                        importance=max(0.4, current.importance * 0.75),
                        dependencies=[]
                    )
                    self.nodes[dep_name] = new_node
                    to_process.append(new_node)
                    
    def get_all_capabilities(self) -> List[Capability]:
        # Return sorted by importance descending
        return sorted(self.nodes.values(), key=lambda c: c.importance, reverse=True)
        
    def get_capability_names(self) -> List[str]:
        return [c.name for c in self.get_all_capabilities()]
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_count": len(self.nodes),
            "nodes": [
                {
                    "name": c.name,
                    "domain": c.domain,
                    "importance": c.importance,
                    "dependencies": c.dependencies
                }
                for c in self.get_all_capabilities()
            ]
        }
