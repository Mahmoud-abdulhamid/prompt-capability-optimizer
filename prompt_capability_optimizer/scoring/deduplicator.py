# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Capability Deduplicator & Context Budgeter
==========================================
Eliminates overlapping capabilities and selects the most specialized, trusted candidates
under strict token and context budgets.
"""

from typing import List, Set
from ..models import Resource
from .scoring_engine import ScoringEngine

class CapabilityDeduplicator:
    
    @classmethod
    def deduplicate(cls, candidates: List[Resource], max_count: int = 3, min_utility: float = 5.0) -> List[Resource]:
        """
        Filters candidates below minimum utility threshold, sorts by rank,
        and prevents activating multiple tools covering the exact same primary capability.
        """
        ranked = ScoringEngine.rank_resources(candidates)
        selected: List[Resource] = []
        covered_capabilities: Set[str] = set()
        
        for res in ranked:
            if res.utility_score < min_utility:
                continue
                
            # Check overlap: does this resource provide already covered capabilities?
            overlap = False
            for cap in res.capabilities:
                if cap in covered_capabilities:
                    overlap = True
                    break
                    
            # If not overlapping or if it provides significant new capability
            if not overlap or len(selected) == 0:
                selected.append(res)
                covered_capabilities.update(res.capabilities)
                
            if len(selected) >= max_count:
                break
                
        return selected
