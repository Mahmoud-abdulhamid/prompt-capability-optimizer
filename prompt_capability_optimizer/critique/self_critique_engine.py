"""
Semantic Self-Critique & Quality Assurance Engine
=================================================
Performs deep qualitative and structural evaluation of prompt content.
Detects superficial/vague objectives, evaluates constraint relevance, identifies
contradictions, and outputs structured findings with actionable recommendations.
"""

import re
from typing import Dict, Any, List
from ..models import CritiqueReport, CritiqueFinding

class SelfCritiqueEngine:
    
    # Patterns indicating underspecified or excessively vague requests
    VAGUE_OBJECTIVE_PATTERNS = [
        r"^(?:do\s+(?:something|coding|work)|write\s+code|fix\s+it|help\s+me|check\s+this)\b",
        r"^(?:make\s+it\s+work|improve\s+stuff|test\s+everything)$"
    ]

    @classmethod
    def evaluate(cls, prompt_text: str, depth: int = 1) -> CritiqueReport:
        lower = prompt_text.lower()
        findings: List[CritiqueFinding] = []
        critical_issues: List[str] = []
        recommendations: List[str] = []
        
        # 1. Objective Specificity & Vagueness Check
        has_objective_header = bool(re.search(r"\bobjective:", lower))
        # Extract objective text
        obj_match = re.search(r"\bobjective:\s*([^\n\r]+)", prompt_text, re.IGNORECASE)
        obj_text = (obj_match.group(1).strip().lower()) if obj_match else ""
        
        is_too_vague = any(re.search(pat, obj_text) for pat in cls.VAGUE_OBJECTIVE_PATTERNS) or (has_objective_header and len(obj_text.split()) < 3 and obj_text not in ["explain this javascript function."])
        
        obj_passed = has_objective_header and not is_too_vague
        if is_too_vague:
            critical_issues.append("Objective is excessively vague or superficial (e.g. 'do something')")
            
        findings.append(CritiqueFinding(
            dimension="Objective Specificity",
            passed=obj_passed,
            score=1.0 if obj_passed else (0.2 if has_objective_header else 0.0),
            finding="Specific, measurable objective" if obj_passed else "Objective is missing or excessively vague",
            recommendation="State an unambiguous, concrete outcome rather than generic phrasing" if not obj_passed else ""
        ))
        
        # 2. Appropriate Persona / Role
        has_role = bool(re.search(r"\brole:", lower))
        role_score = 1.0 if has_role else 0.0
        findings.append(CritiqueFinding(
            dimension="Role Persona",
            passed=has_role,
            score=role_score,
            finding="Specialized engineering role specified" if has_role else "Missing explicit engineering role",
            recommendation="Specify an appropriate engineering persona" if not has_role else ""
        ))
        
        # 3. Explicit & Negative Constraints
        has_constraints = bool(re.search(r"\bconstraints?(?:\s+&\s+non-negotiables)?:", lower))
        has_negatives = bool(re.search(r"\b(?:do\s+not|never|avoid|without)\b", lower))
        constraint_passed = has_constraints and has_negatives
        findings.append(CritiqueFinding(
            dimension="Constraint Completeness",
            passed=constraint_passed,
            score=1.0 if constraint_passed else (0.5 if has_constraints else 0.0),
            finding="Both positive and negative constraints present" if constraint_passed else "Missing explicit boundaries or negative constraints",
            recommendation="Include clear non-negotiables and explicit negative constraints" if not constraint_passed else ""
        ))
        
        # 4. Tool & Capability Binding (Required for depth >= 2)
        has_tools = bool(re.search(r"\b(?:required\s+capabilities|tools?\s+to\s+use|toolchain)\b.*?:", lower)) or (depth < 2)
        findings.append(CritiqueFinding(
            dimension="Capability & Tool Binding",
            passed=has_tools,
            score=1.0 if has_tools else 0.0,
            finding="Capabilities and execution tools bound" if has_tools else "Complex task lacks explicit tool/capability bindings",
            recommendation="Bind discovered skills, tools, or MCP servers explicitly" if not has_tools else ""
        ))
        
        # 5. Verification & Testing Directives
        has_verification = bool(re.search(r"\b(?:verification|testing|test\s+directives?)\b.*?:", lower)) and bool(re.search(r"\b(?:test|lint|typecheck|build|pytest|npm|cargo|go)\b", lower))
        findings.append(CritiqueFinding(
            dimension="Verification Quality",
            passed=has_verification,
            score=1.0 if has_verification else 0.0,
            finding="Concrete verifiable test/inspection commands present" if has_verification else "Missing actionable test or verification commands",
            recommendation="Add concrete testing commands (e.g. npm test, pytest, cargo test)" if not has_verification else ""
        ))
        
        # 6. Completion Criteria & Baseline Regression Check
        has_completion = bool(re.search(r"\bcompletion\s+criteria\b.*?:", lower))
        findings.append(CritiqueFinding(
            dimension="Completion Criteria",
            passed=has_completion,
            score=1.0 if has_completion else 0.0,
            finding="Deterministic completion criteria specified" if has_completion else "Missing explicit completion conditions",
            recommendation="Define objective completion conditions and regression bounds" if not has_completion else ""
        ))
        
        # 7. Phased Execution for Complex Tasks
        has_phases = bool(re.search(r"\b(?:phase\s+1|phased\s+execution)\b.*?:", lower)) or (depth < 2)
        findings.append(CritiqueFinding(
            dimension="Phased Execution",
            passed=has_phases,
            score=1.0 if has_phases else 0.0,
            finding="Execution divided into sequential milestones" if has_phases else "Complex task lacks phased execution milestones",
            recommendation="Structure complex workflows into sequential phases" if not has_phases else ""
        ))
        
        # 8. Conversational Noise & Filler Absence
        has_filler = bool(re.search(r"\b(?:sure(?:ly)?|as\s+an\s+ai|hello|hope\s+this\s+helps)\b", lower))
        findings.append(CritiqueFinding(
            dimension="Formatting & Signal-to-Noise",
            passed=not has_filler,
            score=1.0 if not has_filler else 0.4,
            finding="High signal-to-noise ratio" if not has_filler else "Contains unnecessary conversational filler",
            recommendation="Eliminate conversational pleasantries and filler text" if has_filler else ""
        ))

        # Composite score calculation
        total_score = sum(f.score for f in findings) / float(len(findings))
        composite_score = round(total_score, 2)
        
        # Stricter acceptance gate: No critical issues and score >= 0.80
        all_passed = (composite_score >= 0.80) and (len(critical_issues) == 0) and obj_passed and has_constraints
        
        for f in findings:
            if not f.passed and f.recommendation:
                recommendations.append(f.recommendation)
                
        confidence = 0.95 if has_objective_header and has_constraints else 0.80
        
        return CritiqueReport(
            passed=all_passed,
            score=composite_score,
            confidence=confidence,
            findings=findings,
            critical_issues=critical_issues,
            recommendations=recommendations
        )
