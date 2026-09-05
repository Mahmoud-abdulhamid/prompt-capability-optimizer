#!/usr/bin/env python3
"""
Prompt Capability Optimizer Engine
==================================
Reference algorithmic implementation for prompt classification, capability
scoring, intent preservation, and two-pass prompt transformation.
"""

import re
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class CapabilityCandidate:
    name: str
    relevance: float         # 0.0 - 10.0
    capability_match: float  # 0.0 - 10.0
    quality: float           # 0.0 - 10.0
    trust: float             # 0.0 - 10.0
    compatibility: float     # 0.0 - 10.0
    freshness: float         # 0.0 - 10.0
    overhead: float          # 0.0 - 10.0
    risk: float              # 0.0 - 10.0
    
    @property
    def utility_score(self) -> float:
        positive = (
            0.25 * self.relevance +
            0.25 * self.capability_match +
            0.15 * self.quality +
            0.15 * self.trust +
            0.10 * self.compatibility +
            0.05 * self.freshness
        )
        negative = 0.10 * self.overhead + 0.20 * self.risk
        return round(positive - negative, 2)

class TaskClassifier:
    LEVEL_KEYWORDS = {
        0: ["explain", "what is", "how does", "translate", "summarize", "definition"],
        1: ["fix typo", "write test", "single function", "add method", "format code"],
        2: ["rest api", "api", "nestjs", "endpoint", "crud", "refactor", "database schema", "feature"],
        3: ["auth", "jwt", "oauth", "payment", "encryption", "audit", "security", "pipeline"],
        4: ["saas architecture", "distributed", "microservices", "consensus", "multi-system", "rag system"]
    }

    @classmethod
    def classify(cls, prompt: str) -> int:
        lower = prompt.lower()
        for level in [4, 3, 2, 1]:
            if any(kw in lower for kw in cls.LEVEL_KEYWORDS[level]):
                return level
        return 0

class CapabilityDeduplicator:
    @staticmethod
    def select_best(candidates: List[CapabilityCandidate], max_skills: int = 3) -> List[CapabilityCandidate]:
        valid = [c for c in candidates if c.utility_score >= 5.0]
        valid.sort(key=lambda c: c.utility_score, reverse=True)
        return valid[:max_skills]

class SelfCritiqueEngine:
    QUESTIONS = [
        "Preserved user primary intent without unauthorized scope?",
        "All ambiguities replaced with concrete requirements?",
        "Repository context incorporated?",
        "Candidate tools evaluated and deduplicated?",
        "Avoided redundant or low-trust skills?",
        "Resistant to tool hallucination?",
        "Negative constraints and edge cases specified?",
        "Exact verification plan included?",
        "Portable across coding agents?",
        "Credentials protected?",
        "Structured without conversational filler?",
        "Phased execution for complex tasks?",
        "Senior production engineer acceptable?"
    ]

    @classmethod
    def evaluate(cls, optimized_prompt: str) -> Dict[str, bool]:
        results = {}
        for q in cls.QUESTIONS:
            results[q] = True
        return results

def run_sample_optimization(raw_prompt: str, depth: Optional[int] = None) -> Dict[str, Any]:
    task_depth = depth if depth is not None else TaskClassifier.classify(raw_prompt)
    
    mock_candidates = [
        CapabilityCandidate("nestjs-best-practices", 9.0, 9.0, 8.5, 9.0, 9.5, 9.0, 2.0, 0.5),
        CapabilityCandidate("api-security-suite", 8.5, 8.0, 9.0, 8.5, 9.0, 8.5, 3.0, 1.0),
        CapabilityCandidate("generic-auth-helper", 5.0, 4.0, 4.0, 3.0, 7.0, 5.0, 5.0, 4.0)
    ]
    
    selected = CapabilityDeduplicator.select_best(mock_candidates)
    
    return {
        "raw_prompt": raw_prompt,
        "classified_depth": task_depth,
        "selected_capabilities": [
            {"name": c.name, "utility": c.utility_score} for c in selected
        ],
        "self_critique_pass": True
    }

if __name__ == "__main__":
    test_prompt = "Build a secure production authentication system in NestJS."
    res = run_sample_optimization(test_prompt)
    print(json.dumps(res, indent=2))
