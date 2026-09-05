#!/usr/bin/env python3
"""
P0 and P1 Production Gap Closure Verification Suite
===================================================
Proves that every identified gap between specification and runtime behavior
has been genuinely implemented, integrated, and validated.
"""

import sys
import unittest
import tempfile
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from prompt_capability_optimizer.engine import PromptOptimizerEngine
from prompt_capability_optimizer.discovery.find_skills_adapter import FindSkillsAdapter
from prompt_capability_optimizer.discovery.web_discovery import WebDiscovery, SearchProvider
from prompt_capability_optimizer.discovery.mcp_discovery import McpDiscovery
from prompt_capability_optimizer.adapters.agent_adapters import get_agent_adapter, UnknownAgentAdapter
from prompt_capability_optimizer.critique.self_critique_engine import SelfCritiqueEngine
from prompt_capability_optimizer.security.secret_protector import SecretProtector
from prompt_capability_optimizer.security.trust_engine import TrustEngine
from prompt_capability_optimizer.verification.verification_engine import VerificationEngine
from prompt_capability_optimizer.optimization.semantic_pass import SemanticPass
from prompt_capability_optimizer.models import (
    Resource,
    ResourceType,
    RiskLevel,
    McpServerStatus,
    ClassificationReport
)

class TestProductionGapClosure(unittest.TestCase):

    def setUp(self):
        self.engine = PromptOptimizerEngine()

    # --- P0-1: Real find-skills Pipeline Integration ---
    def test_p0_1_find_skills_integrated_into_pipeline(self):
        # Provide prompt that triggers specialized capability discovery
        raw = "Build a React component with stateful animations."
        # Inject mock search result into find_skills_adapter to verify pipeline integration
        mock_skill = Resource(
            id="find-skills:vercel-labs/agent-skills@motion",
            name="vercel-labs/agent-skills@motion",
            type=ResourceType.SKILL,
            source="skills.sh",
            capabilities=["react-development"],
            trust=9.5,
            reputation=9.5,
            relevance=10.0,
            capability_match=10.0,
            quality=9.0,
            freshness=9.0,
            overhead=1.0,
            risk=0.5
        )
        self.engine.find_skills_adapter._query_cache["react-development"] = [mock_skill]
        
        res = self.engine.optimize(raw, mode="B")
        # Verify that the resource was actually ingested into the registry and selected
        selected_names = [r["name"] for r in res["selected_resources"]]
        self.assertIn("vercel-labs/agent-skills@motion", selected_names, "find-skills result must enter registry and participate in selection")

    # --- P0-2: Real Web Discovery for Unknown Technologies ---
    def test_p0_2_web_discovery_for_unknown_technologies(self):
        # Test discovery for an unseen framework without hardcoded if-statements
        web_engine = WebDiscovery()
        docs = web_engine.discover_for_capability("temporal-workflow-engine")
        self.assertTrue(len(docs) > 0, "Must discover authoritative guidance for novel technology")
        self.assertIn("temporal", docs[0].location.lower())
        self.assertEqual(docs[0].type, ResourceType.DOCUMENTATION)
        self.assertTrue(docs[0].metadata.get("is_reference_data"), "Web docs must be isolated as reference data")

    # --- P0-3: Real MCP Discovery & State Machine ---
    def test_p0_3_mcp_explicit_state_machine(self):
        servers = McpDiscovery.discover()
        self.assertIsInstance(servers, list)
        for s in servers:
            self.assertIn(s.metadata.get("status"), [
                McpServerStatus.CONFIGURED.value,
                McpServerStatus.PARSED.value,
                McpServerStatus.TOOLS_DISCOVERED.value
            ])
            self.assertIn("state_chain", s.metadata)
            self.assertTrue(s.metadata.get("is_untrusted_metadata"), "External MCP metadata must be untrusted")

    # --- P0-4: Cross-Agent Support: Unknown Agent is NOT Gemini ---
    def test_p0_4_unknown_agent_not_silently_gemini(self):
        unknown_adapter = get_agent_adapter("NonExistentAgent99")
        self.assertIsInstance(unknown_adapter, UnknownAgentAdapter, "Unknown agent must return UnknownAgentAdapter")
        self.assertNotEqual(unknown_adapter.get_agent_name(), "gemini_cli", "Unknown agent must NOT silently become Gemini")
        self.assertEqual(unknown_adapter.supports_mcp().status.value, "unknown")
        
        # Test valid agents
        self.assertEqual(get_agent_adapter("claude_code").get_agent_name(), "claude_code")
        self.assertEqual(get_agent_adapter("cursor").get_agent_name(), "cursor")
        self.assertEqual(get_agent_adapter("windsurf").get_agent_name(), "windsurf")
        self.assertEqual(get_agent_adapter("cline").get_agent_name(), "cline")
        self.assertEqual(get_agent_adapter("roo_code").get_agent_name(), "roo_code")

    # --- P0-5: Intent Preservation & Task-Appropriate Role Inference ---
    def test_p0_5_role_inferred_from_task_not_level(self):
        # Educational beginner query should NOT receive Chief Enterprise Architect persona
        role_beg = SemanticPass.infer_task_role("Explain React hooks to a beginner", level=0)
        self.assertIn("Mentor", role_beg)
        self.assertNotIn("Enterprise Architect", role_beg)

        # Performance query
        role_perf = SemanticPass.infer_task_role("Fix the memory leak and profile heap allocations", level=2)
        self.assertIn("Performance", role_perf)

    # --- P0-6: Semantic Self-Critique Rejects Vague Content ---
    def test_p0_6_semantic_critique_rejects_vague_objective(self):
        # A prompt with a header but empty/vague content must FAIL critique
        vague_prompt = """ROLE:
Senior Software Engineer

OBJECTIVE:
do something on the server

CONSTRAINTS & NON-NEGOTIABLES:
- Do not break things

VERIFICATION & TESTING DIRECTIVES:
- npm test
"""
        report = SelfCritiqueEngine.evaluate(vague_prompt, depth=2)
        self.assertFalse(report.passed, "Critique must fail prompts with excessively vague objectives")
        self.assertTrue(any("vague" in issue.lower() for issue in report.critical_issues))

    # --- P0-7: Mode C Execution Governance ---
    def test_p0_7_mode_c_governance(self):
        raw = "Deploy this API and install dependencies"
        # Without explicit confirmation, Mode C must flag AWAITING_USER_APPROVAL
        res_unconfirmed = self.engine.optimize(raw, mode="C", confirmed_execution=False)
        self.assertEqual(res_unconfirmed["mode"], "C")
        self.assertIn("AWAITING_USER_APPROVAL", res_unconfirmed["execution_status"])

        # With explicit confirmation, it transitions to READY_FOR_CONTROLLED_EXECUTION
        res_confirmed = self.engine.optimize(raw, mode="C", confirmed_execution=True)
        self.assertIn("READY_FOR_CONTROLLED_EXECUTION", res_confirmed["execution_status"])

    # --- P1: Secret Protector Never Retains Plaintext Secrets ---
    def test_p1_secret_protector_no_plaintext_leak(self):
        leak_test = "My secret token is sk-1234567890abcdef1234567890abcdef"
        secrets = SecretProtector.find_secrets(leak_test)
        self.assertTrue(len(secrets) > 0)
        for s in secrets:
            self.assertNotIn("full_secret", s, "Must NOT store plaintext secret in result objects")
            self.assertTrue(s["redacted"])
            self.assertIn("...", s["preview"])

    # --- P1: Verification Engine Bun & PNPM Detection ---
    def test_p1_verification_detects_bun_and_pnpm(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "bun.lockb").write_text("", encoding="utf-8")
            (tmp_path / "package.json").write_text(json.dumps({
                "scripts": {"test": "bun test"}
            }), encoding="utf-8")
            
            pm = VerificationEngine.detect_package_manager(tmp_path)
            self.assertEqual(pm, "bun")
            cmds = VerificationEngine.derive_verification_directives(tmp_path)
            self.assertTrue(any("bun test" in c for c in cmds))

    # --- P1: Trust Engine Provenance from Domains ---
    def test_p1_trust_engine_domain_provenance(self):
        doc_res = Resource(
            id="doc:owasp",
            name="OWASP Authentication Cheat Sheet",
            type=ResourceType.DOCUMENTATION,
            source="https://owasp.org",
            capabilities=["auth"],
            metadata={"domain": "owasp.org"}
        )
        trust_eval = TrustEngine.evaluate_resource_trust(doc_res)
        self.assertGreaterEqual(trust_eval["security_trust_score"], 9.5)
        self.assertTrue(any("owasp.org" in factor for factor in trust_eval["trust_factors"]))

if __name__ == "__main__":
    unittest.main()
