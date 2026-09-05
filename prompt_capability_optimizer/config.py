# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Configuration & Threshold Settings
==================================
Central runtime parameters, utility thresholds, discovery limits, and risk tolerances.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class OptimizerConfig:
    # Utility thresholds from references/scoring_rubric.md
    utility_auto_adopt_threshold: float = 7.0
    utility_conditional_threshold: float = 5.0
    
    # Discovery limits
    max_skills_per_prompt: int = 3
    max_skills_level_4: int = 5
    enable_web_discovery: bool = True
    enable_find_skills_cli: bool = True
    
    # Security parameters
    block_high_risk_skills: bool = True
    max_acceptable_skill_risk: float = 6.0
    redact_secrets: bool = True
    
    # Critique parameters
    minimum_critique_pass_score: float = 0.80
    max_correction_iterations: int = 2
    
    # Execution permissions
    allowed_side_effects: List[str] = field(default_factory=lambda: ["NO_SIDE_EFFECT", "LOW_RISK"])
    require_confirmation_for_external_side_effects: bool = True
    
    # Cache settings
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600

DEFAULT_CONFIG = OptimizerConfig()
