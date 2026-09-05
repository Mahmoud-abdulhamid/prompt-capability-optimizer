# Example 05: Security Audit

## 1. Raw User Input
```text
Audit this authentication system.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 3 (Production / High-Risk Security)
- **Primary Intent**: Conduct an exhaustive security audit against OWASP Top 10 and ASVS guidelines, covering password hashing, JWT security, session invalidation, CSRF, timing attacks, rate limiting, and brute-force defenses.
- **Discovered Capabilities**:
  - OWASP Authentication Cheat Sheet standards.
  - Cryptographic verification (Argon2id, bcrypt cost factors, constant-time comparisons).
  - Token analysis (JWT signature algorithms, expiration, rotation, revoking).
- **Output Mode**: Mode B (Optimize + Prepare with Security Matrix).

---

## 3. Optimized Prompt Output

```text
ROLE:
Lead Application Security Engineer & Penetration Testing Specialist

OBJECTIVE:
Perform a comprehensive security audit of the application's authentication and authorization architecture against OWASP ASVS v4.0 standards, identify vulnerabilities, and provide prioritized, code-level remediation directives.

AUDIT SCOPE & THREAT VECTORS:
1. Credential Storage & Hashing:
   - Verify algorithm: Argon2id (m=65536, t=3, p=4) or Bcrypt (work factor >= 12).
   - Check for salt uniqueness and absence of obsolete hashes (MD5, SHA1, plain SHA256).
2. Token & Session Management:
   - JWT Analysis: Algorithm pinning (disallow 'none' and symmetric HS256 when RS256 is expected).
   - Verify token entropy, expiration (short-lived access tokens <= 15m), and refresh token rotation with reuse detection.
   - Storage security: HttpOnly, Secure, SameSite=Strict/Lax cookie flags; no tokens stored in `localStorage`.
3. Brute Force & Denial of Service Protection:
   - Rate limiting on login, registration, and password-reset endpoints.
   - Timing attack prevention: Constant-time comparison (`crypto.timingSafeEqual`) on tokens and passwords to avoid side-channel information leakage.
4. Access Control & Authorization:
   - Privilege escalation (IDOR / BOLA) checks on user-scoped endpoints.
   - Revocation mechanism: Invalidation of active sessions upon password change or logout.

OUTPUT REQUIREMENTS:
Deliver a formal Security Audit Report structured as:
1. Executive Summary & Threat Risk Matrix (Critical, High, Medium, Low).
2. Detailed Findings: Vulnerability description, affected code paths with line references, CVSS v3.1 score, and proof-of-concept attack vector.
3. Production Code Fixes: Drop-in remediation snippets for every identified vulnerability.
4. Automated Regression Tests: Security unit tests validating that patched vulnerabilities cannot reoccur.

VERIFICATION PLAN:
- Static Code Analysis: `npm audit` / `bandit` / `semgrep` scan.
- Test Suite: Automated security tests asserting rejected malformed tokens, timing safety, and rate limit 429 status codes.

COMPLETION CRITERIA:
All audit categories systematically checked; all critical and high findings accompanied by tested code remedies.
```
