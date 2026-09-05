"""
Repository-Aware Verification Engine
====================================
Dynamically derives concrete test, build, lint, and typecheck commands from
actual repository configuration files, guarding against hallucinated tools.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class VerificationEngine:
    
    @classmethod
    def derive_verification_directives(cls, workspace_root: Optional[Path] = None) -> List[str]:
        root = workspace_root or Path.cwd()
        directives: List[str] = []
        
        # 1. Node.js / TypeScript Projects
        pkg_json = root / "package.json"
        if pkg_json.exists() and pkg_json.is_file():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8", errors="replace"))
                scripts = data.get("scripts", {})
                
                # Determine package manager
                pm = "npm"
                if (root / "pnpm-lock.yaml").exists():
                    pm = "pnpm"
                elif (root / "yarn.lock").exists():
                    pm = "yarn"
                elif (root / "bun.lockb").exists():
                    pm = "bun"
                    
                if "test" in scripts:
                    directives.append(f"Execute test suite: {pm} test")
                if "test:e2e" in scripts:
                    directives.append(f"Execute e2e tests: {pm} run test:e2e")
                if "lint" in scripts:
                    directives.append(f"Run linter: {pm} run lint")
                if "build" in scripts:
                    directives.append(f"Run compilation build: {pm} run build")
                if (root / "tsconfig.json").exists():
                    directives.append("Validate TypeScript types: npx tsc --noEmit")
            except Exception:
                pass
                
        # 2. Python Projects
        pyproject = root / "pyproject.toml"
        requirements = root / "requirements.txt"
        if pyproject.exists() or requirements.exists() or any(root.glob("*.py")):
            has_pytest = False
            if pyproject.exists():
                text = pyproject.read_text(encoding="utf-8", errors="replace")
                has_pytest = "pytest" in text
            directives.append("Run unit tests: pytest" if has_pytest else "Run test suite: python -m unittest discover")
            directives.append("Validate Python syntax and imports with standard compiler")

        # 3. Rust Projects
        cargo = root / "Cargo.toml"
        if cargo.exists():
            directives.append("Run test suite: cargo test")
            directives.append("Run static analysis: cargo clippy -- -D warnings")
            directives.append("Verify compilation: cargo check")

        # 4. Go Projects
        gomod = root / "go.mod"
        if gomod.exists():
            directives.append("Run test suite: go test -v ./...")
            directives.append("Verify package compilation: go build ./...")

        # If completely empty or unknown language environment
        if not directives:
            directives = [
                "Execute local automated test suite according to project conventions",
                "Verify zero syntax, compilation, or linter regressions introduced"
            ]
            
        return directives
