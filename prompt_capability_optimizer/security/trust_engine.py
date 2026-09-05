"""
Trust & Provenance Engine
=========================
Separates reputation signals (stars/downloads) from verified security/trust metrics.
Evaluates requested permissions and provenance.
"""

from typing import Dict, Any, List
from ..models import Resource, RiskLevel

class TrustEngine:
    
    VERIFIED_PUBLISHERS = {
        "anthropics", "vercel-labs", "google", "microsoft", "github",
        "nestjs", "facebook", "aws", "docker"
    }

    @classmethod
    def evaluate_resource_trust(cls, resource: Resource) -> Dict[str, Any]:
        """
        Calculates distinct Reputation vs. Trust/Security scores.
        """
        trust_factors = []
        risk_flags = []
        
        # 1. Provenance evaluation
        publisher = resource.name.split("/")[0] if "/" in resource.name else ""
        is_verified_pub = publisher in cls.VERIFIED_PUBLISHERS
        if is_verified_pub:
            trust_factors.append("Verified official organization publisher")
            provenance_score = 9.5
        elif resource.source.startswith("local_builtin"):
            trust_factors.append("Host agent built-in capability")
            provenance_score = 10.0
        elif resource.source.startswith("local"):
            trust_factors.append("Local project/user verified file")
            provenance_score = 8.5
        else:
            provenance_score = 5.0
            
        # 2. Permission and side-effect review
        if any("write" in p.lower() or "exec" in p.lower() or "install" in p.lower() for p in resource.permissions):
            risk_flags.append("Demands write/exec/install permissions")
            permission_penalty = 2.0
        else:
            permission_penalty = 0.0
            
        # Composite security trust score (0.0 to 10.0)
        final_trust = max(1.0, min(10.0, provenance_score - permission_penalty))
        
        # Determine strict RiskLevel
        if "install_required" in resource.permissions:
            risk_level = RiskLevel.EXTERNAL_SIDE_EFFECT
        elif permission_penalty > 0:
            risk_level = RiskLevel.LOW_RISK
        else:
            risk_level = RiskLevel.NO_SIDE_EFFECT
            
        resource.trust = final_trust
        resource.risk_level = risk_level
        
        return {
            "resource_id": resource.id,
            "provenance_score": provenance_score,
            "security_trust_score": final_trust,
            "reputation_score": resource.reputation,
            "risk_level": risk_level.value,
            "trust_factors": trust_factors,
            "risk_flags": risk_flags
        }
