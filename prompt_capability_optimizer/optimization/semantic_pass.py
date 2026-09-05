"""
Pass 1 — Semantic Optimization
==============================
Focuses on intent clarification, objective sharpening, explicit architectural constraints,
and removing ambiguity while strictly preserving user goals.
"""

from typing import Dict, Any, List
from ..models import PromptIR, ClassificationReport

class SemanticPass:
    
    ROLE_MAPPINGS = {
        0: "Senior Systems Engineer & Technical Explainer",
        1: "Staff Software Engineer & Testing Specialist",
        2: "Principal Software Architect & Full-Stack Engineer",
        3: "Lead Application Security Architect & Cryptography Specialist",
        4: "Chief Enterprise Architect & Distributed Systems Engineer"
    }

    @classmethod
    def execute(cls, prompt_ir: PromptIR, classification: ClassificationReport) -> PromptIR:
        # 1. Assign precise persona
        prompt_ir.role = cls.ROLE_MAPPINGS.get(classification.level, "Senior Software Architect")
        prompt_ir.depth = classification.level
        
        # 2. Add baseline engineering constraints
        baseline_constraints = [
            "Additive Change Policy: Preserve existing working functionality and shared contracts.",
            "Strict Typing: Ensure zero implicit 'any' and validate all schema boundaries."
        ]
        for c in baseline_constraints:
            if c not in prompt_ir.constraints:
                prompt_ir.constraints.append(c)
                prompt_ir.diff.added_constraints.append(c)
                
        # 3. Add explicit negative constraints
        negative_rules = [
            "Do NOT introduce unapproved third-party dependencies.",
            "Do NOT remove or bypass existing security or linting configurations."
        ]
        for nr in negative_rules:
            if nr not in prompt_ir.negative_constraints:
                prompt_ir.negative_constraints.append(nr)
                
        # 4. Formulate completion criteria
        prompt_ir.completion_criteria = [
            "All new and existing automated tests pass with 0 errors and 0 warnings.",
            "Code conforms cleanly to existing repository conventions and style rules."
        ]
        
        prompt_ir.diff.preserved_intent_summary = f"Preserved intent: '{prompt_ir.objective}'"
        return prompt_ir
