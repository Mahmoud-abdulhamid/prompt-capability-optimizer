"""
Core Data Models and Normalized Schemas
=======================================
Defines common dataclasses for capabilities, discovered resources, host runtime
specifications, prompt intermediate representations, and critique results.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum

class ResourceType(str, Enum):
    SKILL = "skill"
    MCP = "mcp"
    CONNECTOR = "connector"
    PLUGIN = "plugin"
    BUILTIN_TOOL = "tool"
    WEB_RESOURCE = "web_resource"
    DOCUMENTATION = "documentation"

class CapabilityStatus(str, Enum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"
    HOST_DECLARED = "host_declared"
    RUNTIME_DETECTED = "runtime_detected"
    INFERRED = "inferred"

class McpServerStatus(str, Enum):
    CONFIGURED = "CONFIGURED"
    PARSED = "PARSED"
    REACHABLE = "REACHABLE"
    INITIALIZED = "INITIALIZED"
    TOOLS_DISCOVERED = "TOOLS_DISCOVERED"

class RiskLevel(str, Enum):
    NO_SIDE_EFFECT = "NO_SIDE_EFFECT"
    LOW_RISK = "LOW_RISK"
    EXTERNAL_SIDE_EFFECT = "EXTERNAL_SIDE_EFFECT"
    DESTRUCTIVE = "DESTRUCTIVE"

class RequirementCategory(str, Enum):
    USER_EXPLICIT = "USER_EXPLICIT"
    DERIVED_NECESSITY = "DERIVED_NECESSITY"
    PROJECT_CONSTRAINT = "PROJECT_CONSTRAINT"
    SECURITY_REQUIREMENT = "SECURITY_REQUIREMENT"
    VERIFICATION_REQUIREMENT = "VERIFICATION_REQUIREMENT"
    OPTIONAL_RECOMMENDATION = "OPTIONAL_RECOMMENDATION"

@dataclass
class ClassifiedRequirement:
    text: str
    category: RequirementCategory
    source: str = "intent"

@dataclass
class Capability:
    name: str
    domain: str = "general"
    importance: float = 1.0  # 0.0 - 1.0
    dependencies: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class Resource:
    id: str
    name: str
    type: ResourceType
    source: str  # local, registry, host, web
    capabilities: List[str] = field(default_factory=list)
    location: Optional[str] = None
    relevance: float = 5.0          # 0.0 - 10.0
    capability_match: float = 5.0   # 0.0 - 10.0
    quality: float = 5.0            # 0.0 - 10.0
    trust: float = 5.0              # 0.0 - 10.0 (security/integrity)
    reputation: float = 5.0         # 0.0 - 10.0 (stars/downloads/community)
    compatibility: float = 8.0      # 0.0 - 10.0
    freshness: float = 5.0          # 0.0 - 10.0
    overhead: float = 2.0           # 0.0 - 10.0
    risk: float = 1.0               # 0.0 - 10.0
    risk_level: RiskLevel = RiskLevel.LOW_RISK
    permissions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def utility_score(self) -> float:
        """
        Authoritative formula from references/scoring_rubric.md:
        Utility = (0.25*R + 0.25*M + 0.15*Q + 0.15*T + 0.10*C + 0.05*F) - (0.10*O + 0.20*K)
        """
        pos = (
            0.25 * self.relevance +
            0.25 * self.capability_match +
            0.15 * self.quality +
            0.15 * self.trust +
            0.10 * self.compatibility +
            0.05 * self.freshness
        )
        neg = (0.10 * self.overhead) + (0.20 * self.risk)
        return round(pos - neg, 3)

@dataclass
class HostCapabilityItem:
    capability: str
    status: CapabilityStatus
    confidence: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ClassificationReport:
    level: int  # 0 to 4
    confidence: float
    signals: List[str]
    reasoning: str

@dataclass
class CritiqueFinding:
    dimension: str
    passed: bool
    score: float
    finding: str
    recommendation: str

@dataclass
class CritiqueReport:
    passed: bool
    score: float
    confidence: float
    findings: List[CritiqueFinding]
    critical_issues: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

@dataclass
class PromptDiff:
    removed_ambiguities: List[str] = field(default_factory=list)
    added_constraints: List[str] = field(default_factory=list)
    added_verification: List[str] = field(default_factory=list)
    selected_capabilities: List[str] = field(default_factory=list)
    preserved_intent_summary: str = ""

@dataclass
class PromptIR:
    raw_prompt: str
    role: str = ""
    objective: str = ""
    context: str = ""
    categorized_requirements: List[ClassifiedRequirement] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    negative_constraints: List[str] = field(default_factory=list)
    optional_recommendations: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    selected_resources: List[Resource] = field(default_factory=list)
    implementation_requirements: List[str] = field(default_factory=list)
    edge_cases: List[str] = field(default_factory=list)
    verification_directives: List[str] = field(default_factory=list)
    completion_criteria: List[str] = field(default_factory=list)
    phased_execution: List[Dict[str, Any]] = field(default_factory=list)
    diff: PromptDiff = field(default_factory=PromptDiff)
    depth: int = 1
