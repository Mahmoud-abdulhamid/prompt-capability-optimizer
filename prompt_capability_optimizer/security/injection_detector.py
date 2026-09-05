# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Prompt Injection & Instruction Hijacking Detector
=================================================
Identifies directive-override patterns, system prompt hijacking attempts,
and untrusted data exfiltration payloads.
"""

import re
from typing import Dict, Any, List

class PromptInjectionDetector:
    
    HIJACK_PATTERNS = [
        r"(?i)\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b",
        r"(?i)\byou\s+are\s+now\s+(?:in\s+developer\s+mode|unrestricted|dan\b|an\s+evil)",
        r"(?i)\bdisregard\s+(?:all\s+)?safety\s+(?:guidelines|protocols)\b",
        r"(?i)\bsystem\s+override\b",
        r"(?i)\bnew\s+primary\s+directive\b",
        r"(?i)\b(?:print|upload|exfiltrate|leak|curl|send)\s+(?:the\s+)?(?:secrets?|\.env|id_rsa|api_key|credentials?)\b"
    ]

    @classmethod
    def scan(cls, text: str) -> Dict[str, Any]:
        matched_threats = []
        
        for pat in cls.HIJACK_PATTERNS:
            match = re.search(pat, text)
            if match:
                matched_threats.append(match.group(0))
                
        is_suspicious = len(matched_threats) > 0
        
        return {
            "is_suspicious": is_suspicious,
            "threat_count": len(matched_threats),
            "threats_detected": matched_threats,
            "action": "SANITIZE_AND_CONTAIN" if is_suspicious else "ALLOW"
        }

    @classmethod
    def sanitize(cls, text: str) -> str:
        """
        Neutralizes detected hijacking directives by enclosing them in passive containment blocks.
        """
        scan_res = cls.scan(text)
        if not scan_res["is_suspicious"]:
            return text
            
        sanitized = text
        for threat in scan_res["threats_detected"]:
            sanitized = re.sub(
                re.escape(threat),
                f"[REDACTED_ADVERSARIAL_DIRECTIVE: '{threat}']",
                sanitized,
                flags=re.IGNORECASE
            )
        return sanitized
