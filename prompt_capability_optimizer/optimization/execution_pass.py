# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Pass 2 — Execution Optimization
===============================
Binds selected capabilities, discovered tools, phased execution milestones,
and repository-aware verification directives.
"""

from typing import List, Dict, Any
from ..models import PromptIR, Resource

class ExecutionPass:
    
    @classmethod
    def execute(cls, prompt_ir: PromptIR, selected_resources: List[Resource], verification_cmds: List[str]) -> PromptIR:
        prompt_ir.selected_resources = selected_resources
        prompt_ir.diff.selected_capabilities = [r.name for r in selected_resources]
        
        # 1. Bind Verification Commands
        prompt_ir.verification_directives = verification_cmds
        prompt_ir.diff.added_verification = verification_cmds
        
        # 2. Build Phased Milestones (for Level >= 2)
        if prompt_ir.depth >= 2:
            prompt_ir.phased_execution = [
                {
                    "phase": 1,
                    "title": "Baseline Inspection",
                    "goal": "Verify existing tests and repository conventions prior to modification."
                },
                {
                    "phase": 2,
                    "title": "Contract & Schema Definition",
                    "goal": "Establish immutable interfaces, DTOs, and validation boundaries."
                },
                {
                    "phase": 3,
                    "title": "Core Implementation",
                    "goal": "Implement business logic following additive change standards."
                },
                {
                    "phase": 4,
                    "title": "Verification & Static Analysis",
                    "goal": "Run typechecking, unit/e2e tests, and regression verification."
                }
            ]
        else:
            prompt_ir.phased_execution = []
            
        return prompt_ir
