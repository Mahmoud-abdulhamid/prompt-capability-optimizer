"""
Prompt Capability Optimizer
===========================
Autonomous, cross-agent prompt optimization and capability discovery framework.
"""

from .models import (
    Capability,
    Resource,
    ResourceType,
    PromptIR,
    CritiqueReport,
    ClassificationReport
)
from .config import OptimizerConfig, DEFAULT_CONFIG
from .engine import PromptOptimizerEngine

__version__ = "1.0.0"
__author__ = "Mahmoud Abdelhameid"
__email__ = "Develper.net@gmail.com"
__linkedin__ = "https://www.linkedin.com/in/mahmoud-abdelhameid-dev/"
__copyright__ = "Copyright (c) 2026 Mahmoud Abdelhameid. All rights reserved."
__license__ = "MIT"

__all__ = [
    "PromptOptimizerEngine",
    "OptimizerConfig",
    "DEFAULT_CONFIG",
    "Capability",
    "Resource",
    "ResourceType",
    "PromptIR",
    "CritiqueReport",
    "ClassificationReport"
]
