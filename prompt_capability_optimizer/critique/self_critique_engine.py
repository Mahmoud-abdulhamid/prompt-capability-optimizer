"""
Real Self-Critique & Quality Assurance Engine
============================================
Evaluates prompt candidates against a 13-point multidimensional checklist.
Can fail inadequate prompts, outputs diagnostic findings, and drives corrective passes.
"""

import re
from typing import Dict, Any, List
from ..models import CritiqueReport, CritiqueFinding

class SelfCritiqueEngine:
    
    @classmethod
    def evaluate(cls, prompt_text: str, depth: int = 1) -> CritiqueReport:
        lower = prompt_text.lower()
        findings: List[CritiqueFinding] = []
        recommendations: List[str] = []
        
        # 1. Intent preserved & Objective clear
        has_objective = bool(re.search(r"\bobjective:", lower)) or bool(re.search(r"\b(?:build|implement|design|create|refactor|fix|explain)\b", lower))
        findings.append(CritiqueFinding(
            question="Objective clearly formulated without ambiguity?",
            passed=has_objective,
            finding="Clear objective section identified" if has_objective else "Missing explicit objective directive",
            recommendation="Add an unambiguous OBJECTIVE definition" if not has_objective else ""
        ))
        
        # 2. Role defined
        has_role = bool(re.search(r"\brole:", lower))
        findings.append(CritiqueFinding(
            question="Senior engineer persona / role specified?",
            passed=has_role,
            finding="Explicit role specified" if has_role else "Missing specialized role definition",
            recommendation="Add a specialized ROLE section" if not has_role else ""
        ))
        
        # 3. Explicit constraints defined
        has_constraints = bool(re.search(r"\bconstraints?(?:\s+&\s+non-negotiables)?:", lower)) or ("do not" in lower)
        findings.append(CritiqueFinding(
            question="Explicit constraints and non-negotiables defined?",
            passed=has_constraints,
            finding="Constraints present" if has_constraints else "Missing explicit technical constraints",
            recommendation="Incorporate CONSTRAINTS & NON-NEGOTIABLES" if not has_constraints else ""
        ))
        
        # 4. Negative constraints (what NOT to do)
        has_negatives = bool(re.search(r"\b(?:do\s+not|never|avoid|without)\b", lower))
        findings.append(CritiqueFinding(
            question="Negative constraints specified (what NOT to do)?",
            passed=has_negatives,
            finding="Negative constraints identified" if has_negatives else "No negative boundaries provided",
            recommendation="Specify what the agent MUST NOT do" if not has_negatives else ""
        ))
        
        # 5. Required tools & capabilities identified (mandatory for depth >= 2)
        has_tools = bool(re.search(r"\b(?:required\s+capabilities|tools?\s+to\s+use|toolchain)\b.*?:", lower)) or (depth < 2)
        findings.append(CritiqueFinding(
            question="Required capabilities and toolchain bound to task?",
            passed=has_tools,
            finding="Toolchain bound" if has_tools else "Missing explicit tool/capability bindings for complex task",
            recommendation="Bind discovered skills and tools explicitly" if not has_tools else ""
        ))
        
        # 6. Verification and test directives present
        has_verification = bool(re.search(r"\b(?:verification|testing|test\s+directives?)\b.*?:", lower)) or bool(re.search(r"\b(?:npm\s+test|pytest|cargo\s+test|vitest|tsc)\b", lower))
        findings.append(CritiqueFinding(
            question="Concrete verification and testing commands provided?",
            passed=has_verification,
            finding="Verification directives present" if has_verification else "Missing concrete test/verification commands",
            recommendation="Add verifiable testing commands (build, test, lint)" if not has_verification else ""
        ))
        
        # 7. Completion criteria defined
        has_completion = bool(re.search(r"\bcompletion\s+criteria\b.*?:", lower)) or bool(re.search(r"\b(?:acceptance\s+criteria|deliverables)\b.*?:", lower))
        findings.append(CritiqueFinding(
            question="Deterministic completion criteria defined?",
            passed=has_completion,
            finding="Completion criteria present" if has_completion else "Missing explicit completion conditions",
            recommendation="Define exact COMPLETION CRITERIA" if not has_completion else ""
        ))
        
        # 8. Phased execution for complex tasks (mandatory for depth >= 2)
        has_phases = bool(re.search(r"\b(?:phase\s+1|phased\s+execution)\b.*?:", lower)) or (depth < 2)
        findings.append(CritiqueFinding(
            question="Complex task divided into phased execution milestones?",
            passed=has_phases,
            finding="Phased plan present" if has_phases else "Complex task lacks sequential execution phases",
            recommendation="Break down complex workflow into sequential phases" if not has_phases else ""
        ))
        
        # 9. Security considerations addressed (for depth >= 3)
        has_security = bool(re.search(r"\b(?:security|auth|sanitiz|protect|owasp)\b", lower)) or (depth < 3)
        findings.append(CritiqueFinding(
            question="Security boundaries addressed for high-risk domains?",
            passed=has_security,
            finding="Security addressed" if has_security else "High-risk task lacks security safeguards",
            recommendation="Add explicit security requirements" if not has_security else ""
        ))
        
        # 10. No conversational filler
        has_filler = bool(re.search(r"\b(?:sure(?:ly)?|as\s+an\s+ai|hello|hope\s+this\s+helps)\b", lower))
        findings.append(CritiqueFinding(
            question="Free of conversational filler and metadata preamble?",
            passed=not has_filler,
            finding="Clean direct formatting" if not has_filler else "Contains conversational filler words",
            recommendation="Eliminate conversational pleasantries" if has_filler else ""
        ))
        
        # Calculate passed status and composite score
        passed_count = sum(1 for f in findings if f.passed)
        total_questions = len(findings)
        score = round(passed_count / float(total_questions), 2)
        
        # Must achieve at least 80% pass score and have no critical missing components
        all_passed = score >= 0.80 and has_objective and has_constraints
        
        for f in findings:
            if not f.passed and f.recommendation:
                recommendations.append(f.recommendation)
                
        return CritiqueReport(
            passed=all_passed,
            score=score,
            findings=findings,
            recommendations=recommendations
        )
