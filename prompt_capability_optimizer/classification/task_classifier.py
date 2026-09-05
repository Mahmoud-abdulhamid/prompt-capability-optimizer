# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Hybrid Task Classifier
======================
Combines structural signals, risk level, multi-system count, and architectural scope
with an explainable confidence report.
"""

import re
from typing import List, Dict, Any, Tuple
from ..models import ClassificationReport

class TaskClassifier:
    
    LEVEL_4_PATTERNS = [
        r"\b(?:saas|multi-tenant|distributed|microservices|consensus|event-driven|cqrs|high-availability|rag\s+(?:architecture|evaluation|system)|enterprise\s+architecture)\b",
        r"\b(?:multi-system|cross-service|data\s+pipeline|warehouse|lakehouse)\b"
    ]
    
    LEVEL_3_PATTERNS = [
        r"\b(?:auth|authentication|oauth|oidc|jwt|saml|sso|argon2|bcrypt|cryptography|session\s+management)\b",
        r"\b(?:payment|stripe|billing|webhook\s+security|audit\s+log|penetration\s+test|vulnerability|owasp|asvs)\b",
        r"\b(?:production|compliance|secret\s+management|rbac|abac|rate\s+limiting|ddos)\b"
    ]
    
    LEVEL_2_PATTERNS = [
        r"\b(?:rest\s+api|graphql|grpc|api|endpoint|crud|database\s+schema|migration|prisma|typeorm|drizzle|postgres|redis)\b",
        r"\b(?:refactor|architecture|module|service|repository\s+pattern|clean\s+architecture|feature)\b",
        r"\b(?:memory\s+leak|profiling|concurrency|race\s+condition|deadlock|performance\s+optimization)\b"
    ]
    
    LEVEL_1_PATTERNS = [
        r"\b(?:fix\s+bug|write\s+test|unit\s+test|add\s+method|function|format|lint|typecheck|single\s+file)\b",
        r"\b(?:regex|helper|utility|script|component|button|form)\b"
    ]
    
    LEVEL_0_PATTERNS = [
        r"^(?:explain|what\s+is|how\s+does|why\s+does|describe|translate|summarize|definition\s+of)\b",
        r"\b(?:explain\s+this|walkthrough|overview)\b"
    ]

    @classmethod
    def classify(cls, prompt: str) -> ClassificationReport:
        lower_prompt = prompt.lower().strip()
        signals = []
        
        # Check Level 4 (Research / Multi-System / Enterprise SaaS)
        l4_matches = [m.group(0) for pat in cls.LEVEL_4_PATTERNS for m in re.finditer(pat, lower_prompt)]
        if l4_matches:
            signals.extend(l4_matches)
            return ClassificationReport(
                level=4,
                confidence=0.92,
                signals=signals,
                reasoning=f"Identified high-level multi-system architectural signals: {', '.join(set(signals))}"
            )
            
        # Check Level 3 (Production / High-Risk / Security & Payment)
        l3_matches = [m.group(0) for pat in cls.LEVEL_3_PATTERNS for m in re.finditer(pat, lower_prompt)]
        if l3_matches:
            signals.extend(l3_matches)
            return ClassificationReport(
                level=3,
                confidence=0.88,
                signals=signals,
                reasoning=f"Identified security, financial, or high-risk production vectors: {', '.join(set(signals))}"
            )
            
        # Check Level 2 (Complex / Multi-File Feature / API / Refactor)
        l2_matches = [m.group(0) for pat in cls.LEVEL_2_PATTERNS for m in re.finditer(pat, lower_prompt)]
        if l2_matches:
            signals.extend(l2_matches)
            return ClassificationReport(
                level=2,
                confidence=0.85,
                signals=signals,
                reasoning=f"Identified feature implementation, API design, or multi-file refactoring: {', '.join(set(signals))}"
            )
            
        # Check Level 0 (Informational / Explanation)
        l0_matches = [m.group(0) for pat in cls.LEVEL_0_PATTERNS for m in re.finditer(pat, lower_prompt)]
        if l0_matches and len(lower_prompt.split()) <= 15:
            signals.extend(l0_matches)
            return ClassificationReport(
                level=0,
                confidence=0.95,
                signals=signals,
                reasoning=f"Identified brief informational or conceptual query: {', '.join(set(signals))}"
            )
            
        # Check Level 1 (Moderate / Local Fix / Unit Test)
        l1_matches = [m.group(0) for pat in cls.LEVEL_1_PATTERNS for m in re.finditer(pat, lower_prompt)]
        if l1_matches:
            signals.extend(l1_matches)
            return ClassificationReport(
                level=1,
                confidence=0.80,
                signals=signals,
                reasoning=f"Identified single-module edit or standard unit task: {', '.join(set(signals))}"
            )

        # Fallback based on length and sentence structure
        word_count = len(lower_prompt.split())
        if word_count > 40:
            return ClassificationReport(
                level=2,
                confidence=0.65,
                signals=["long_prompt_heuristic"],
                reasoning="Classified as Level 2 due to extensive prompt scope and specification density."
            )
        elif word_count < 8:
            return ClassificationReport(
                level=0,
                confidence=0.70,
                signals=["short_prompt_heuristic"],
                reasoning="Classified as Level 0 due to concise informational phrasing."
            )
        else:
            return ClassificationReport(
                level=1,
                confidence=0.60,
                signals=["standard_task_default"],
                reasoning="Classified as Level 1 standard engineering task by default."
            )
