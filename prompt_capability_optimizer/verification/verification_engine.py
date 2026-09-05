# Copyright (c) 2026 Mahmoud (Develper.net@gmail.com). All rights reserved.
# Licensed under the MIT License.

"""
Repository-Aware Verification Engine
====================================
Dynamically derives concrete test, build, lint, and typecheck commands from
actual repository configuration files, lockfiles, and declared scripts.
Prioritizes project-declared commands and guards against hallucinated toolchains.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

class VerificationEngine:
    
    @classmethod
    def detect_package_manager(cls, root: Path) -> str:
        # Check modern lockfiles in order of precedence
        if (root / "bun.lockb").exists() or (root / "bun.lock").exists():
            return "bun"
        if (root / "pnpm-lock.yaml").exists():
            return "pnpm"
        if (root / "yarn.lock").exists():
            return "yarn"
        return "npm"

    @classmethod
    def derive_verification_directives(cls, workspace_root: Optional[Path] = None) -> List[str]:
        root = workspace_root or Path.cwd()
        directives: List[str] = []
        
        # 1. Node.js / JavaScript / TypeScript Projects
        pkg_json = root / "package.json"
        if pkg_json.exists() and pkg_json.is_file():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8", errors="replace"))
                scripts = data.get("scripts", {})
                pm = cls.detect_package_manager(root)
                
                if "test" in scripts:
                    directives.append(f"Execute project test runner: {pm} test")
                elif "test:unit" in scripts:
                    directives.append(f"Execute unit tests: {pm} run test:unit")
                    
                if "test:e2e" in scripts:
                    directives.append(f"Execute e2e integration suite: {pm} run test:e2e")
                    
                if "lint" in scripts:
                    directives.append(f"Run code linter: {pm} run lint")
                    
                if "build" in scripts:
                    directives.append(f"Run compilation build: {pm} run build")
                    
                # Only require typecheck if tsconfig exists AND typescript is installed/scripted
                if (root / "tsconfig.json").exists():
                    if "typecheck" in scripts:
                        directives.append(f"Validate types: {pm} run typecheck")
                    else:
                        directives.append("Validate TypeScript types: npx tsc --noEmit")
            except Exception:
                pass
                
        # 2. Python Projects
        pyproject = root / "pyproject.toml"
        poetry_lock = root / "poetry.lock"
        requirements = root / "requirements.txt"
        
        if pyproject.exists() or requirements.exists() or poetry_lock.exists() or any(root.glob("*.py")):
            if poetry_lock.exists():
                directives.append("Execute Python tests: poetry run pytest")
            elif pyproject.exists():
                text = pyproject.read_text(encoding="utf-8", errors="replace")
                if "pytest" in text:
                    directives.append("Execute Python tests: pytest")
                else:
                    directives.append("Execute Python tests: python -m unittest discover")
            else:
                directives.append("Execute Python test suite: python -m unittest discover")
                
            directives.append("Verify Python syntax and imports with standard compiler")

        # 3. Rust Projects
        cargo = root / "Cargo.toml"
        if cargo.exists():
            directives.append("Execute Rust test suite: cargo test")
            directives.append("Run static analysis: cargo clippy -- -D warnings")
            directives.append("Verify compilation: cargo check")

        # 4. Go Projects
        gomod = root / "go.mod"
        if gomod.exists():
            directives.append("Execute Go test suite: go test -v ./...")
            directives.append("Verify package compilation: go build ./...")

        # Baseline regression guard
        directives.append("Verify zero new regressions introduced against pre-existing repository baseline")

        return directives
