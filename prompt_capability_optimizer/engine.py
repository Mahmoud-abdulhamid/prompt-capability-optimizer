# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Prompt Capability Optimizer Core Engine
=======================================
End-to-end execution pipeline connecting classification, capability graph,
discovery, trust evaluation, two-pass optimization, self-critique, and Mode C lifecycle.
"""

from typing import Dict, Any, List, Optional
from .models import PromptIR, Resource, ClassificationReport, CritiqueReport, RiskLevel
from .config import DEFAULT_CONFIG, OptimizerConfig
from .classification.task_classifier import TaskClassifier
from .intent.intent_analyzer import IntentAnalyzer
from .capabilities.extractor import CapabilityExtractor
from .capabilities.graph import CapabilityGraph
from .discovery.registry import ResourceRegistry
from .discovery.local_discovery import LocalSkillDiscovery
from .discovery.mcp_discovery import McpDiscovery
from .discovery.web_discovery import WebDiscovery
from .discovery.find_skills_adapter import FindSkillsAdapter
from .security.trust_engine import TrustEngine
from .security.injection_detector import PromptInjectionDetector
from .security.secret_protector import SecretProtector
from .scoring.deduplicator import CapabilityDeduplicator
from .verification.verification_engine import VerificationEngine
from .optimization.optimizer import TwoPassOptimizer
from .critique.self_critique_engine import SelfCritiqueEngine

class PromptOptimizerEngine:
    
    def __init__(self, config: Optional[OptimizerConfig] = None):
        self.config = config or DEFAULT_CONFIG
        self.registry = ResourceRegistry()
        self.find_skills_adapter = FindSkillsAdapter()
        self.web_discovery = WebDiscovery()
        
    def _populate_discovery(self, required_caps: List[str], depth: int):
        # 1. Real local skill discovery
        local_skills = LocalSkillDiscovery.discover()
        self.registry.register_many(local_skills)
        
        # 2. Real host MCP discovery with parsed state machine
        mcp_servers = McpDiscovery.discover()
        self.registry.register_many(mcp_servers)
        
        # 3. Real find-skills integration: query for specialized capabilities
        if depth >= 1 and self.config.enable_find_skills_cli:
            for cap_name in required_caps:
                # Query open skills ecosystem for packages matching capability
                skills_results = self.find_skills_adapter.search(cap_name, limit=2)
                if skills_results:
                    self.registry.register_many(skills_results)
                    
        # 4. Real Web Discovery pipeline for dynamic/unseen technologies
        if depth >= 1 and self.config.enable_web_discovery:
            for cap_name in required_caps:
                web_docs = self.web_discovery.discover_for_capability(cap_name)
                if web_docs:
                    self.registry.register_many(web_docs)
                
    def optimize(self, raw_prompt: str, mode: str = "B", confirmed_execution: bool = False) -> Dict[str, Any]:
        """
        Executes the full pipeline:
        Intent -> Classify -> Capabilities -> Discovery -> Scoring -> Two-Pass Optimization -> Critique -> Mode C Governance -> Output
        """
        # Step 0: Security Sanity Check (Secret protection & Prompt Injection Detection)
        secrets_found = SecretProtector.find_secrets(raw_prompt)
        safe_prompt = SecretProtector.redact(raw_prompt)
        injection_scan = PromptInjectionDetector.scan(safe_prompt)
        if injection_scan["is_suspicious"]:
            safe_prompt = PromptInjectionDetector.sanitize(safe_prompt)

        # Step 1: Classification & Intent
        classification = TaskClassifier.classify(safe_prompt)
        intent_data = IntentAnalyzer.analyze(safe_prompt)
        
        # Step 2: Capability Extraction & Graph
        caps = CapabilityExtractor.extract_capabilities(safe_prompt)
        cap_graph = CapabilityGraph(caps)
        required_cap_names = cap_graph.get_capability_names()
        
        # Step 3: Real Discovery (Local, find-skills, MCP, Web)
        self.registry.clear()
        self._populate_discovery(required_cap_names, classification.level)
        
        # Step 4: Capability Matching & Trust Evaluation
        matched_resources: List[Resource] = []
        for cap_name in required_cap_names:
            found = self.registry.find_by_capability(cap_name)
            for r in found:
                TrustEngine.evaluate_resource_trust(r)
                if r not in matched_resources:
                    matched_resources.append(r)
                    
        # Step 5: Scoring, Filtering & Deduplication
        max_skills = self.config.max_skills_level_4 if classification.level >= 4 else self.config.max_skills_per_prompt
        selected_resources = CapabilityDeduplicator.deduplicate(
            matched_resources,
            max_count=max_skills,
            min_utility=self.config.utility_conditional_threshold
        )
        
        # Ensure at least baseline agent execution tool is bound for complex tasks if none was discovered
        if not selected_resources and classification.level >= 2:
            selected_resources.append(Resource(
                id="builtin:native-agent-tools",
                name="Native Host Agent Execution Tools",
                type=ResourceType.BUILTIN_TOOL,
                source="host_runtime",
                capabilities=["filesystem-access", "shell-execution"],
                relevance=8.0,
                capability_match=8.0,
                quality=9.0,
                trust=10.0,
                reputation=10.0,
                compatibility=10.0,
                freshness=10.0,
                overhead=1.0,
                risk=0.0,
                risk_level=RiskLevel.NO_SIDE_EFFECT
            ))
        
        # Step 6: Dynamic Repository Verification
        verification_directives = VerificationEngine.derive_verification_directives()
        
        # Step 7: Two-Pass Optimization
        prompt_ir = TwoPassOptimizer.optimize(
            raw_prompt=safe_prompt,
            classification=classification,
            selected_resources=selected_resources,
            verification_cmds=verification_directives
        )
        rendered_prompt = TwoPassOptimizer.render_prompt(prompt_ir)
        
        # Step 8: Real Qualitative Self-Critique
        critique_report = SelfCritiqueEngine.evaluate(rendered_prompt, depth=classification.level)
        
        # Step 9: Automatic Correction Pass (if critique indicates missing requirements)
        if not critique_report.passed:
            for rec in critique_report.recommendations:
                if "negative" in rec.lower():
                    prompt_ir.negative_constraints.append("Do NOT alter unrequested codebase layers.")
                if "completion" in rec.lower():
                    prompt_ir.completion_criteria.append("100% of integration checks pass against baseline.")
            rendered_prompt = TwoPassOptimizer.render_prompt(prompt_ir)
            # Re-evaluate
            critique_report = SelfCritiqueEngine.evaluate(rendered_prompt, depth=classification.level)
            
        # Step 10: Mode C Lifecycle & Governance Check
        execution_status = "NOT_REQUESTED"
        if mode.upper() == "C":
            task_has_side_effects = any(kw in safe_prompt.lower() for kw in ["install", "deploy", "delete", "drop", "publish", "push", "remove", "migrate"])
            resource_has_side_effects = any(r.risk_level in [RiskLevel.EXTERNAL_SIDE_EFFECT, RiskLevel.DESTRUCTIVE] for r in selected_resources)
            has_side_effects = task_has_side_effects or resource_has_side_effects
            
            if has_side_effects and not confirmed_execution:
                execution_status = "AWAITING_USER_APPROVAL (Side-effects detected; explicit confirmation required)"
            else:
                execution_status = "READY_FOR_CONTROLLED_EXECUTION"

        return {
            "mode": mode.upper(),
            "execution_status": execution_status,
            "classification": {
                "level": classification.level,
                "confidence": classification.confidence,
                "signals": classification.signals,
                "reasoning": classification.reasoning
            },
            "required_capabilities": required_cap_names,
            "selected_resources": [
                {
                    "name": r.name,
                    "type": r.type.value,
                    "utility_score": r.utility_score,
                    "trust": r.trust,
                    "source": r.source,
                    "risk_level": r.risk_level.value
                }
                for r in selected_resources
            ],
            "security": {
                "secrets_redacted": len(secrets_found),
                "injection_threats_neutralized": len(injection_scan["threats_detected"])
            },
            "critique": {
                "passed": critique_report.passed,
                "score": critique_report.score,
                "confidence": critique_report.confidence,
                "critical_issues": critique_report.critical_issues,
                "recommendations": critique_report.recommendations
            },
            "diff": {
                "added_constraints": prompt_ir.diff.added_constraints,
                "selected_capabilities": prompt_ir.diff.selected_capabilities,
                "verification_directives": prompt_ir.diff.added_verification
            },
            "optimized_prompt": rendered_prompt
        }
