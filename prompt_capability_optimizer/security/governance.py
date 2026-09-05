# Copyright (c) 2026 Mahmoud Abdelhameid (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Installation Governance & Permission Gate
=========================================
Enforces the 'Never Install Blindly' mandate and governs tool invocation side-effects.
"""

from typing import Dict, Any, Optional
from ..models import Resource, RiskLevel

class InstallationGovernance:
    
    @classmethod
    def evaluate_installation(cls, resource: Resource) -> Dict[str, Any]:
        """
        Calculates whether a discovered external capability may be recommended or installed.
        Decision rule: Expected Value > (Risk + Overhead)
        """
        expected_value = (resource.capability_match * 0.4) + (resource.quality * 0.3) + (resource.relevance * 0.3)
        cost_and_risk = (resource.risk * 0.6) + (resource.overhead * 0.4)
        
        approved_for_recommendation = expected_value > cost_and_risk and resource.trust >= 6.0
        requires_explicit_user_consent = resource.risk_level in [
            RiskLevel.EXTERNAL_SIDE_EFFECT,
            RiskLevel.DESTRUCTIVE
        ]
        
        return {
            "resource_name": resource.name,
            "expected_value": round(expected_value, 2),
            "cost_and_risk": round(cost_and_risk, 2),
            "approved_for_recommendation": approved_for_recommendation,
            "requires_explicit_user_consent": requires_explicit_user_consent,
            "risk_level": resource.risk_level.value,
            "governance_decision": (
                "REQUIRE_USER_APPROVAL" if requires_explicit_user_consent else
                ("ADOPT" if approved_for_recommendation else "REJECT")
            )
        }
