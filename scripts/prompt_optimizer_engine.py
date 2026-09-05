# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

#!/usr/bin/env python3
"""
Prompt Capability Optimizer Engine CLI Bridge
=============================================
Reference implementation bridge connecting to the core package engine.
Eliminates mock data, executes real capability discovery, and performs real critique.
"""

import sys
import json
from pathlib import Path

# Add parent directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from prompt_capability_optimizer.engine import PromptOptimizerEngine
from prompt_capability_optimizer.classification.task_classifier import TaskClassifier
from prompt_capability_optimizer.critique.self_critique_engine import SelfCritiqueEngine
from prompt_capability_optimizer.scoring.deduplicator import CapabilityDeduplicator
from prompt_capability_optimizer.models import Resource

def run_sample_optimization(raw_prompt: str, depth: int = None):
    engine = PromptOptimizerEngine()
    result = engine.optimize(raw_prompt, mode="B")
    return {
        "raw_prompt": raw_prompt,
        "classified_depth": result["classification"]["level"],
        "selected_capabilities": result["selected_resources"],
        "self_critique_pass": result["critique"]["passed"],
        "critique_score": result["critique"]["score"],
        "optimized_prompt": result["optimized_prompt"]
    }

if __name__ == "__main__":
    test_prompt = "Build a secure production authentication system in NestJS."
    res = run_sample_optimization(test_prompt)
    print(json.dumps(res, indent=2))
