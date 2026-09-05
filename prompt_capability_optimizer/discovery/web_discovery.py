"""
Authoritative Web Discovery Pipeline
====================================
Performs capability-driven search targeting verified upstream documentation,
official repositories, and architectural standards.
"""

from typing import List, Dict, Any, Optional
from ..models import Resource, ResourceType, RiskLevel

class WebDiscovery:
    
    AUTHORITATIVE_DOMAINS = {
        "docs.nestjs.com": 9.5,
        "nodejs.org": 9.5,
        "typescriptlang.org": 9.5,
        "react.dev": 9.5,
        "owasp.org": 9.8,
        "postgresql.org": 9.5,
        "redis.io": 9.5,
        "github.com": 8.0
    }

    @classmethod
    def discover_guidance(cls, capability_query: str) -> List[Resource]:
        """
        Derives targeted authoritative documentation resources for specialized capabilities.
        """
        query_clean = capability_query.lower().strip()
        resources: List[Resource] = []
        
        # Match against known upstream authoritative portals
        if "nestjs" in query_clean:
            resources.append(Resource(
                id="doc:nestjs-official",
                name="NestJS Official Architecture Guide",
                type=ResourceType.DOCUMENTATION,
                source="https://docs.nestjs.com",
                capabilities=["nestjs-development", "api-design"],
                location="https://docs.nestjs.com/techniques/authentication",
                relevance=9.0,
                capability_match=9.0,
                quality=9.5,
                trust=9.5,
                reputation=9.8,
                compatibility=10.0,
                freshness=9.5,
                overhead=1.0,
                risk=0.0,
                risk_level=RiskLevel.NO_SIDE_EFFECT,
                metadata={"domain": "docs.nestjs.com", "verified": True}
            ))
            
        if "auth" in query_clean or "security" in query_clean or "jwt" in query_clean:
            resources.append(Resource(
                id="doc:owasp-asvs",
                name="OWASP ASVS Authentication Standard",
                type=ResourceType.DOCUMENTATION,
                source="https://owasp.org",
                capabilities=["authentication-architecture", "security-auditing"],
                location="https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html",
                relevance=9.5,
                capability_match=9.5,
                quality=10.0,
                trust=9.8,
                reputation=10.0,
                compatibility=10.0,
                freshness=9.0,
                overhead=1.0,
                risk=0.0,
                risk_level=RiskLevel.NO_SIDE_EFFECT,
                metadata={"domain": "owasp.org", "verified": True}
            ))
            
        if "react" in query_clean:
            resources.append(Resource(
                id="doc:react-official",
                name="React Official Documentation",
                type=ResourceType.DOCUMENTATION,
                source="https://react.dev",
                capabilities=["react-development", "ui-component-design"],
                location="https://react.dev/learn",
                relevance=9.0,
                capability_match=9.0,
                quality=9.5,
                trust=9.5,
                reputation=9.9,
                compatibility=10.0,
                freshness=9.5,
                overhead=1.0,
                risk=0.0,
                risk_level=RiskLevel.NO_SIDE_EFFECT,
                metadata={"domain": "react.dev", "verified": True}
            ))
            
        if "redis" in query_clean:
            resources.append(Resource(
                id="doc:redis-official",
                name="Redis Streams Architecture Specification",
                type=ResourceType.DOCUMENTATION,
                source="https://redis.io",
                capabilities=["redis-caching-streaming", "in-memory-caching"],
                location="https://redis.io/docs/data-types/streams/",
                relevance=9.5,
                capability_match=9.5,
                quality=9.5,
                trust=9.8,
                reputation=9.8,
                compatibility=10.0,
                freshness=9.5,
                overhead=1.0,
                risk=0.0,
                risk_level=RiskLevel.NO_SIDE_EFFECT,
                metadata={"domain": "redis.io", "verified": True}
            ))

        if "go" in query_clean or "golang" in query_clean:
            resources.append(Resource(
                id="doc:go-official",
                name="Go Standard Library & Concurrency Patterns",
                type=ResourceType.DOCUMENTATION,
                source="https://go.dev",
                capabilities=["go-development", "concurrency"],
                location="https://go.dev/doc/",
                relevance=9.0,
                capability_match=9.0,
                quality=9.8,
                trust=10.0,
                reputation=10.0,
                compatibility=10.0,
                freshness=9.5,
                overhead=1.0,
                risk=0.0,
                risk_level=RiskLevel.NO_SIDE_EFFECT,
                metadata={"domain": "go.dev", "verified": True}
            ))
            
        return resources
