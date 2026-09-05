"""
Two-Pass Optimizer Orchestrator
===============================
Coordinates semantic and execution passes, formats final structured prompts,
and renders concise prompt diffs.
"""

from typing import List, Dict, Any
from ..models import PromptIR, Resource, ClassificationReport
from .semantic_pass import SemanticPass
from .execution_pass import ExecutionPass

class TwoPassOptimizer:
    
    @classmethod
    def optimize(
        cls,
        raw_prompt: str,
        classification: ClassificationReport,
        selected_resources: List[Resource],
        verification_cmds: List[str]
    ) -> PromptIR:
        # Initialize PromptIR
        prompt_ir = PromptIR(
            raw_prompt=raw_prompt,
            objective=raw_prompt.strip(),
            depth=classification.level
        )
        
        # Pass 1: Semantic Clarification
        prompt_ir = SemanticPass.execute(prompt_ir, classification)
        
        # Pass 2: Execution Binding
        prompt_ir = ExecutionPass.execute(prompt_ir, selected_resources, verification_cmds)
        
        return prompt_ir

    @classmethod
    def render_prompt(cls, ir: PromptIR) -> str:
        """
        Renders PromptIR into canonical prompt format.
        """
        lines = []
        lines.append(f"ROLE:\n{ir.role}\n")
        lines.append(f"OBJECTIVE:\n{ir.objective}\n")
        
        if ir.context:
            lines.append(f"CONTEXT & REPO STATE:\n{ir.context}\n")
            
        if ir.constraints or ir.negative_constraints:
            lines.append("CONSTRAINTS & NON-NEGOTIABLES:")
            for c in ir.constraints:
                lines.append(f"- {c}")
            for nc in ir.negative_constraints:
                lines.append(f"- {nc}")
            lines.append("")
            
        if ir.selected_resources:
            lines.append("REQUIRED CAPABILITIES & TOOLS:")
            for r in ir.selected_resources:
                lines.append(f"- {r.name} ({r.type.value} from {r.source})")
            lines.append("")
            
        if ir.phased_execution:
            lines.append("PHASED EXECUTION PLAN:")
            for p in ir.phased_execution:
                lines.append(f"Phase {p['phase']} — {p['title']}: {p['goal']}")
            lines.append("")
            
        if ir.verification_directives:
            lines.append("VERIFICATION & TESTING DIRECTIVES:")
            for v in ir.verification_directives:
                lines.append(f"- {v}")
            lines.append("")
            
        if ir.completion_criteria:
            lines.append("COMPLETION CRITERIA:")
            for cc in ir.completion_criteria:
                lines.append(f"- {cc}")
            lines.append("")
            
        return "\n".join(lines).strip()
