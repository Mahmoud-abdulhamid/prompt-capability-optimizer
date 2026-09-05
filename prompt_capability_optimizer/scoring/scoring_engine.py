"""
Authoritative Scoring Engine
============================
The SINGLE source of truth for capability utility calculations, directly implementing
the mathematical formula established in references/scoring_rubric.md.
"""

from typing import List
from ..models import Resource

class ScoringEngine:
    
    @classmethod
    def calculate_utility(cls, resource: Resource) -> float:
        """
        Formula:
        Utility = (0.25*R + 0.25*M + 0.15*Q + 0.15*T + 0.10*C + 0.05*F) - (0.10*O + 0.20*K)
        """
        return resource.utility_score

    @classmethod
    def rank_resources(cls, resources: List[Resource]) -> List[Resource]:
        """
        Sorts candidates by utility score descending.
        Tie-breaking: Higher Trust -> Higher Quality -> Lower Overhead.
        """
        return sorted(
            resources,
            key=lambda r: (r.utility_score, r.trust, r.quality, -r.overhead),
            reverse=True
        )
