"""
Trust & Provenance Engine
=========================
Separates reputation signals (stars/downloads) from verified security/trust metrics.
Evaluates requested permissions, publisher domain provenance, and metadata.
"""

from typing import Dict, Any, List
from ..models import Resource, RiskLevel, ResourceType

class TrustEngine:
    
    VERIFIED_PUBLISHERS = {
        "anthropics", "vercel-labs", "google", "microsoft", "github",
        "nestjs", "facebook", "aws", "docker", "composiohq"
    }
    
    TRUSTED_DOMAINS = {
        "docs.nestjs.com", "owasp.org", "react.dev", "go.dev", "python.org",
        "typescriptlang.org", "nodejs.org", "postgresql.org", "redis.io",
        "kafka.apache.org", "temporal.io", "neon.tech", "prisma.io"
    }

    @classmethod
    def evaluate_resource_trust(cls, resource: Resource) -> Dict[str, Any]:
        """
        Calculates distinct Reputation vs. Trust/Security scores using domain provenance and metadata.
        """
        trust_factors = []
        risk_flags = []
        provenance_score = 5.0
        
        # 1. Provenance from official domains (for Web Documentation)
        domain = resource.metadata.get("domain", "")
        if not domain and resource.location:
            import urllib.parse
            try:
                domain = urllib.parse.urlparse(resource.location).hostname or ""
            except Exception:
                domain = ""
                
        if domain in cls.TRUSTED_DOMAINS or any(domain.endswith(f".{td}") for td in cls.TRUSTED_DOMAINS):
            trust_factors.append(f"Verified authoritative technical domain ({domain})")
            provenance_score = 9.8
        elif resource.type == ResourceType.DOCUMENTATION:
            if domain.endswith(".org") or domain.endswith(".dev") or domain.endswith(".io"):
                provenance_score = 8.5
            else:
                provenance_score = 7.0

        # 2. Provenance from publisher names (for skills/packages)
        publisher = resource.name.split("/")[0] if "/" in resource.name else ""
        if publisher.lower() in cls.VERIFIED_PUBLISHERS:
            trust_factors.append(f"Verified official ecosystem publisher ({publisher})")
            provenance_score = max(provenance_score, 9.5)
            
        if resource.source.startswith("local_builtin"):
            trust_factors.append("Host agent built-in capability")
            provenance_score = 10.0
        elif resource.source.startswith("local"):
            trust_factors.append("Local project/user verified file")
            provenance_score = max(provenance_score, 8.5)
            
        # 3. Permission and side-effect review
        if any("write" in p.lower() or "exec" in p.lower() or "install" in p.lower() for p in resource.permissions):
            risk_flags.append("Demands write/exec/install permissions")
            permission_penalty = 1.5
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
            
        resource.trust = round(final_trust, 2)
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
