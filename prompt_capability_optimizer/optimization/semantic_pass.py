# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Pass 1 — Semantic Optimization & Intent Preservation
====================================================
Infers accurate personas from actual task content rather than arbitrary level numbers.
Categorizes requirements into USER_EXPLICIT, PROJECT_CONSTRAINT, SECURITY_REQUIREMENT,
and OPTIONAL_RECOMMENDATION without inventing unrequested mandatory burdens.
"""

import re
from typing import Dict, Any, List
from ..models import PromptIR, ClassificationReport, ClassifiedRequirement, RequirementCategory

class SemanticPass:

    @classmethod
    def infer_task_role(cls, prompt_text: str, level: int) -> str:
        """
        Derives an appropriate role from actual task content instead of arbitrary level tier.
        """
        lower = prompt_text.lower()
        
        # Beginner or educational queries
        if re.search(r"\b(?:beginner|explain|tutorial|what is|how does)\b", lower):
            return "Technical Mentor & Software Specialist"
            
        # Security & Auth domains
        if re.search(r"\b(?:auth|authentication|oauth|jwt|security|crypto|asvs|penetration)\b", lower):
            return "Application Security & Authentication Specialist"
            
        # Performance & Memory
        if re.search(r"\b(?:memory leak|profiling|heap|garbage collect|latency|optimization)\b", lower):
            return "Runtime Performance & Diagnostics Specialist"
            
        # Frontend & UI
        if re.search(r"\b(?:react|vue|ui|frontend|css|tailwind|playwright|cypress)\b", lower):
            return "Frontend Systems & QA Automation Engineer"
            
        # Backend & APIs
        if re.search(r"\b(?:nestjs|fastify|express|rest api|graphql|grpc|endpoint|microservices)\b", lower):
            return "Backend Services & API Architect"
            
        # Multi-System SaaS
        if level >= 4 or "saas" in lower or "multi-tenant" in lower:
            return "Distributed Systems & Cloud Architect"
            
        # General engineering default
        return "Senior Software Engineer"

    @classmethod
    def execute(cls, prompt_ir: PromptIR, classification: ClassificationReport) -> PromptIR:
        # 1. Assign specialized persona based on actual task domain
        prompt_ir.role = cls.infer_task_role(prompt_ir.raw_prompt, classification.level)
        prompt_ir.depth = classification.level
        
        # 2. Extract and categorize requirements
        classified_reqs: List[ClassifiedRequirement] = []
        
        # A. USER_EXPLICIT
        classified_reqs.append(ClassifiedRequirement(
            text=prompt_ir.objective,
            category=RequirementCategory.USER_EXPLICIT
        ))
        
        # B. PROJECT_CONSTRAINT (respecting existing repo language and style)
        repo_rule = "Follow the repository's existing language standards, compiler settings, and architectural patterns."
        classified_reqs.append(ClassifiedRequirement(
            text=repo_rule,
            category=RequirementCategory.PROJECT_CONSTRAINT
        ))
        if repo_rule not in prompt_ir.constraints:
            prompt_ir.constraints.append(repo_rule)
            prompt_ir.diff.added_constraints.append(repo_rule)
            
        additive_rule = "Additive Change Policy: Preserve existing working functionality and public contracts."
        classified_reqs.append(ClassifiedRequirement(
            text=additive_rule,
            category=RequirementCategory.PROJECT_CONSTRAINT
        ))
        if additive_rule not in prompt_ir.constraints:
            prompt_ir.constraints.append(additive_rule)
            prompt_ir.diff.added_constraints.append(additive_rule)
            
        # C. SECURITY_REQUIREMENT
        if classification.level >= 3 or any(w in prompt_ir.raw_prompt.lower() for w in ["auth", "security", "token", "password", "payment"]):
            sec_rule = "Security: Sanitize all untrusted inputs, parameterize queries, and prevent credential exposure."
            classified_reqs.append(ClassifiedRequirement(
                text=sec_rule,
                category=RequirementCategory.SECURITY_REQUIREMENT
            ))
            if sec_rule not in prompt_ir.constraints:
                prompt_ir.constraints.append(sec_rule)
                
        # D. NEGATIVE CONSTRAINTS (Preventing unrequested scope changes)
        negative_rules = [
            "Do NOT introduce unapproved third-party dependencies.",
            "Do NOT modify unrelated modules or existing configurations."
        ]
        for nr in negative_rules:
            if nr not in prompt_ir.negative_constraints:
                prompt_ir.negative_constraints.append(nr)
                
        # E. COMPLETION CRITERIA (emphasizing baseline regression prevention)
        prompt_ir.completion_criteria = [
            "All targeted functionality behaves as requested with zero regression against pre-existing baseline.",
            "Code adheres strictly to project linting, typechecking, and formatting rules."
        ]
        
        prompt_ir.categorized_requirements = classified_reqs
        prompt_ir.diff.preserved_intent_summary = f"Preserved user intent: '{prompt_ir.objective}'"
        return prompt_ir
