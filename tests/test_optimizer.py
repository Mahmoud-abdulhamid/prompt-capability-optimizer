#!/usr/bin/env python3
"""
Comprehensive Quality Gate & Skill Verification Suite
=====================================================
Validates all requirements, schema integrity, multi-archetype test coverage,
and cross-agent compatibility for prompt-capability-optimizer.
"""

import os
import sys
import json
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class TestPromptCapabilityOptimizer(unittest.TestCase):
    
    def test_01_core_skill_file_exists(self):
        skill_file = BASE_DIR / "SKILL.md"
        self.assertTrue(skill_file.exists(), "SKILL.md must exist at root")
        content = skill_file.read_text(encoding="utf-8")
        self.assertIn("name: prompt-capability-optimizer", content)
        self.assertIn("description:", content)
        self.assertIn("Phase 1: Intent Analysis", content)
        self.assertIn("Phase 2: Capability Discovery", content)
        self.assertIn("Never Install Blindly", content)

    def test_02_directory_structure(self):
        expected_dirs = ["adapters", "references", "templates", "scripts", "examples", "tests"]
        for d in expected_dirs:
            target = BASE_DIR / d
            self.assertTrue(target.is_dir(), f"Directory {d} must exist")

    def test_03_references_completeness(self):
        expected_refs = [
            "capability_graph.md",
            "prompt_engineering_standards.md",
            "scoring_rubric.md",
            "security_and_trust.md",
            "cross_agent_matrix.md"
        ]
        for ref in expected_refs:
            p = BASE_DIR / "references" / ref
            self.assertTrue(p.exists(), f"Reference {ref} must exist")
            self.assertGreater(p.stat().st_size, 500, f"Reference {ref} must not be empty or superficial")

    def test_04_adapters_and_schemas(self):
        schema_file = BASE_DIR / "adapters" / "host_capabilities.json"
        adapter_doc = BASE_DIR / "adapters" / "environment_adapters.md"
        self.assertTrue(schema_file.exists())
        self.assertTrue(adapter_doc.exists())
        
        # Validate json syntax
        with open(schema_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertIn("properties", data)
            self.assertIn("capabilities", data["properties"])

    def test_05_templates_integrity(self):
        templates = [
            "optimized_prompt_template.md",
            "execution_plan_template.md",
            "verification_matrix_template.md"
        ]
        for t in templates:
            p = BASE_DIR / "templates" / t
            self.assertTrue(p.exists(), f"Template {t} must exist")
            self.assertGreater(p.stat().st_size, 300)

    def test_06_examples_coverage_all_8_categories(self):
        examples = [
            "01_simple_prompt.md",
            "02_coding_api.md",
            "03_existing_repo_refactor.md",
            "04_debugging_memory_leak.md",
            "05_security_audit.md",
            "06_complex_saas_architecture.md",
            "07_research_rag_evaluation.md",
            "08_multitool_issue_resolver.md"
        ]
        for ex in examples:
            p = BASE_DIR / "examples" / ex
            self.assertTrue(p.exists(), f"Example {ex} must exist")
            content = p.read_text(encoding="utf-8")
            self.assertIn("Raw User Input", content)
            self.assertIn("Optimized Prompt", content)

    def test_07_scripts_functionality(self):
        sys.path.insert(0, str(BASE_DIR / "scripts"))
        import capability_checker
        import prompt_optimizer_engine
        
        rep = capability_checker.generate_report()
        self.assertIn("agent_identity", rep)
        self.assertIn("runtime_environment", rep)
        self.assertIn("capabilities", rep)
        
        # Test engine
        res = prompt_optimizer_engine.run_sample_optimization("Build NestJS API")
        self.assertEqual(res["classified_depth"], 2)
        self.assertTrue(res["self_critique_pass"])

    def test_08_quality_gate_checklist(self):
        skill_content = (BASE_DIR / "SKILL.md").read_text(encoding="utf-8")
        checks = [
            "find-skills",
            "prompt-engineering",
            "Never Install Blindly",
            "Two-Level",
            "Self-Critique",
            "Mode A",
            "Mode B",
            "Mode C"
        ]
        for c in checks:
            self.assertIn(c, skill_content, f"Checklist item '{c}' must be present in SKILL.md")

if __name__ == "__main__":
    unittest.main()
