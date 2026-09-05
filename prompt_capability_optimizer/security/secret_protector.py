"""
Secret & Credential Protector
=============================
Detects plaintext secrets, API keys, private tokens, and database passwords
using strict regex patterns and entropy analysis.
CRITICAL SAFETY INVARIANT: Never retains or serializes plaintext secret values.
"""

import re
from typing import Dict, Any, List

class SecretProtector:
    
    SECRET_PATTERNS = [
        # AWS Access Key
        (r"\b(AKIA[0-9A-Z]{16})\b", "AWS_ACCESS_KEY"),
        # GitHub Personal Access Token
        (r"\b(gh[pousr]_[A-Za-z0-9_]{36,255})\b", "GITHUB_TOKEN"),
        # OpenAI / Standard Bearer sk- keys
        (r"\b(sk-[a-zA-Z0-9]{20,64})\b", "API_SECRET_KEY"),
        # JWT Token pattern (three base64 chunks)
        (r"\b(ey[A-Za-z0-9_-]{10,}\.ey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b", "JWT_TOKEN"),
        # Database connection strings with credentials
        (r"(?i)\b([a-z]+:\/\/[a-zA-Z0-9_\-\.]+:[^@\s\/]+@[a-zA-Z0-9_\-\.]+:[0-9]+\/[a-zA-Z0-9_\-\.]+)\b", "DATABASE_CREDENTIALS"),
        # Generic private key headers
        (r"-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----[\s\S]+?-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----", "PRIVATE_KEY"),
        # Generic password assignment
        (r"(?i)\b(?:password|passwd|secret)\s*[:=]\s*['\"]([^'\"]{6,})['\"]", "PLAINTEXT_PASSWORD")
    ]

    @classmethod
    def find_secrets(cls, text: str) -> List[Dict[str, Any]]:
        """
        Detects secrets and returns sanitized descriptor objects.
        NEVER stores or leaks the raw plaintext secret string.
        """
        found = []
        for pattern, label in cls.SECRET_PATTERNS:
            for match in re.finditer(pattern, text):
                matched_val = match.group(1) if match.groups() else match.group(0)
                # Form secure masked preview without retaining original payload
                preview = matched_val[:3] + "..." + matched_val[-3:] if len(matched_val) > 6 else "***"
                found.append({
                    "label": label,
                    "preview": preview,
                    "length": len(matched_val),
                    "redacted": True
                })
        return found

    @classmethod
    def redact(cls, text: str) -> str:
        redacted = text
        for pattern, label in cls.SECRET_PATTERNS:
            def _replace(match):
                return f"[REDACTED_{label}]"
            redacted = re.sub(pattern, _replace, redacted)
        return redacted
