# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Capability Extractor
====================
Extracts technical capability requirements from task descriptions using an
engineering domain ontology.
"""

import re
from typing import List, Set, Dict
from ..models import Capability

class CapabilityExtractor:
    
    # Domain ontology mappings: pattern -> (canonical_capability, domain, dependencies)
    ONTOLOGY = {
        # Backend & APIs
        r"\bnestjs\b": ("nestjs-development", "backend", ["typescript", "api-design"]),
        r"\brest\s+api\b": ("rest-api-design", "backend", ["http-protocol"]),
        r"\bgraphql\b": ("graphql-api", "backend", ["schema-design"]),
        r"\bgrpc\b": ("grpc-services", "backend", ["protobuf"]),
        r"\bfastify\b": ("fastify-framework", "backend", ["nodejs"]),
        r"\bexpress\b": ("express-framework", "backend", ["nodejs"]),
        
        # Frontend & UI
        r"\breact\b": ("react-development", "frontend", ["javascript", "ui-component-design"]),
        r"\bplaywright\b": ("playwright-testing", "testing", ["e2e-testing", "browser-automation"]),
        r"\bvue\b": ("vue-development", "frontend", ["ui-component-design"]),
        r"\bnext\.?js\b": ("nextjs-framework", "fullstack", ["react-development"]),
        r"\btailwind\b": ("tailwind-css", "frontend", ["css-styling"]),
        
        # Security & Auth
        r"\b(?:auth|authentication)\b": ("authentication-architecture", "security", ["credential-handling", "session-security"]),
        r"\boauth(?:2(?:\.0)?)?\b": ("oauth-oidc-integration", "security", ["authentication-architecture", "token-management"]),
        r"\bjwt\b": ("jwt-token-management", "security", ["cryptography", "token-security"]),
        r"\brbac\b": ("role-based-access-control", "security", ["authorization-logic"]),
        r"\brate\s+limit(?:ing)?\b": ("rate-limiting", "security", ["dos-prevention"]),
        r"\b(?:audit|security\s+audit)\b": ("security-auditing", "security", ["vulnerability-assessment", "owasp-asvs"]),
        r"\bargon2\b": ("argon2-password-hashing", "security", ["cryptographic-storage"]),
        r"\bbcrypt\b": ("bcrypt-password-hashing", "security", ["cryptographic-storage"]),
        
        # Data & Storage
        r"\bpostgres(?:ql)?\b": ("postgresql-database", "database", ["relational-modeling", "sql-optimization"]),
        r"\bredis\b": ("redis-caching-streaming", "database", ["in-memory-caching"]),
        r"\bprisma\b": ("prisma-orm", "database", ["database-migrations", "type-safe-querying"]),
        r"\btypeorm\b": ("typeorm", "database", ["database-migrations"]),
        r"\bmongo(?:db)?\b": ("mongodb-database", "database", ["document-modeling"]),
        
        # Testing & QA
        r"\b(?:testing|tests?)\b": ("automated-testing", "quality", ["test-runner"]),
        r"\bunit\s+tests?\b": ("unit-testing", "quality", ["mocking", "assertion-framework"]),
        r"\be2e\s+tests?\b": ("e2e-testing", "quality", ["integration-testing"]),
        r"\bjest\b": ("jest-framework", "quality", ["unit-testing"]),
        r"\bpytest\b": ("pytest-framework", "quality", ["python-testing"]),
        r"\bvitest\b": ("vitest-framework", "quality", ["unit-testing"]),
        
        # Architecture & Systems
        r"\bmulti-tenant\b": ("multi-tenant-architecture", "architecture", ["data-isolation", "tenant-scoping"]),
        r"\bsaas\b": ("saas-architecture", "architecture", ["billing-integration", "multi-tenant-architecture"]),
        r"\brag\b": ("rag-architecture", "ai_ml", ["vector-search", "document-retrieval", "embeddings"]),
        r"\bmemory\s+leak\b": ("memory-leak-diagnostics", "performance", ["heap-profiling", "v8-diagnostics"]),
        r"\brefactor(?:ing)?\b": ("architectural-refactoring", "architecture", ["dependency-inversion", "code-smells"])
    }

    @classmethod
    def extract_capabilities(cls, text: str) -> List[Capability]:
        lower_text = text.lower()
        extracted: Dict[str, Capability] = {}
        
        for pattern, (name, domain, deps) in cls.ONTOLOGY.items():
            if re.search(pattern, lower_text):
                extracted[name] = Capability(
                    name=name,
                    domain=domain,
                    importance=0.9,
                    dependencies=deps,
                    description=f"Requires specialized knowledge in {name}"
                )
                
        # If no domain capability matched, provide baseline software engineering capability
        if not extracted:
            extracted["software-engineering-fundamentals"] = Capability(
                name="software-engineering-fundamentals",
                domain="general",
                importance=0.5,
                dependencies=[],
                description="Core software development and reasoning skills"
            )
            
        return list(extracted.values())
