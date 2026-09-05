# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Semantic Intent Analyzer
========================
Dissects user prompts into primary intent, explicit constraints, input expectations,
and required deliverables while guarding against intent alteration.
"""

import re
from typing import Dict, Any, List

class IntentAnalyzer:
    
    ACTION_VERBS = [
        "build", "create", "implement", "design", "refactor", "fix",
        "debug", "audit", "optimize", "test", "explain", "review", "migrate"
    ]
    
    @classmethod
    def analyze(cls, raw_prompt: str) -> Dict[str, Any]:
        cleaned = raw_prompt.strip()
        lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        
        primary_intent = lines[0] if lines else cleaned
        action_verb = "execute"
        for v in cls.ACTION_VERBS:
            if re.search(rf"\b{v}\b", primary_intent, re.IGNORECASE):
                action_verb = v.lower()
                break
                
        # Detect explicit user constraints (e.g., using ..., with ..., do not ...)
        constraints = []
        negative_constraints = []
        
        # Look for negative directives
        neg_matches = re.findall(r"\b(?:do not|don't|never|without|avoid)\s+([^,.;\n]+)", cleaned, re.IGNORECASE)
        for nm in neg_matches:
            negative_constraints.append(f"Do not {nm.strip()}")
            
        # Look for explicit technology or pattern constraints
        tech_matches = re.findall(r"\b(?:using|with|in)\s+([A-Za-z0-9_\-\+\#\.\s]+?)(?:,|\.|\n|and|$)", cleaned, re.IGNORECASE)
        for tm in tech_matches:
            item = tm.strip()
            if len(item) > 1 and item.lower() not in ["the", "a", "an", "this", "these"]:
                constraints.append(f"Utilize {item}")

        # Formulate a crisp objective sentence
        objective = primary_intent
        if not objective.endswith("."):
            objective += "."
            
        return {
            "primary_intent": primary_intent,
            "action_verb": action_verb,
            "objective": objective,
            "explicit_constraints": constraints,
            "negative_constraints": negative_constraints,
            "raw_text": cleaned
        }
