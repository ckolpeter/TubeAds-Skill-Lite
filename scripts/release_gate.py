#!/usr/bin/env python3
"""Static release checks + SHA256 inventory. Not a sandbox or malware scanner."""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IGNORE_PARTS = {".git", "__pycache__", ".venv", "output"}
ALLOWED_RUNTIME_IMPORTS = {"argparse", "sys", "pathlib", "html", "json", "math", "re", "unicodedata", "uuid",
                           "datetime", "decimal", "urllib.parse", "typing", "__future__", "core", "platform_rules"}
REQUIRED = ["SKILL.md", "README.md", "AGENTS.md", "CLAUDE.md", "LICENSE", "skill.json", "scripts/core.py",
            "scripts/toolkit.py", "scripts/platform_rules.py", "schemas/brief.schema.json", "schemas/plan.schema.json",
            "examples/brief.synthetic.json", "examples/expected/plan.json", "docs/HANDOFF.md", "docs/TEST_REPORT.md",
            "evals/manual-cases.md", "tests/test_toolkit.py"]


def inventory(root: Path = ROOT) -> list[Path]:
    return sorted(p for p in root.rglob("*") if p.is_file() and not any(part in IGNORE_PARTS for part in p.relative_to(root).parts)
                  and p.name not in {"MANIFEST.sha256", ".DS_Store"} and p.suffix != ".pyc")


def structural_errors(root: Path = ROOT) -> list[str]:
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append("Missing required file: " + name)
    try:
        cfg = json.loads((root / "skill.json").read_text(encoding="utf-8"))
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        if not skill.startswith("---\n"):
            errors.append("SKILL.md frontmatter missing")
        name = re.search(r"^name: (.+)$", skill, re.M)
        desc = re.search(r"^description: (.+)$", skill, re.M)
        if not name or name.group(1) != cfg["id"] or name.group(1).casefold() != root.name.casefold():
            errors.append("Skill ID must match directory and metadata")
        if not desc or not 1 <= len(desc.group(1)) <= 1024:
            errors.append("Skill description length invalid")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", cfg["id"]):
            errors.append("Skill ID format invalid")
        for key in ("runtime_network", "external_reads", "external_writes"):
            if cfg.get(key) is not False:
                errors.append("Offline boundary changed: " + key)
        for p in (root / "scripts").rglob("*.py"):
            if p.name == "release_gate.py":
                continue
            tree = ast.parse(p.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                modules = [alias.name for alias in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) else []
                for module in modules:
                    if module not in ALLOWED_RUNTIME_IMPORTS:
                        errors.append("Unapproved runtime import in " + p.name)
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                    errors.append("Dynamic execution forbidden in " + p.name)
        for p in root.rglob("*"):
            if any(part in IGNORE_PARTS for part in p.relative_to(root).parts):
                continue
            if p.is_symlink():
                errors.append("Release may not contain symlinks")
            if p.name == ".env" or p.name.startswith(".env."):
                errors.append("Environment files must not be shipped")
    except (OSError, ValueError, KeyError, SyntaxError) as exc:
        errors.append("Invalid package metadata/source: " + type(exc).__name__)
    return errors


def manifest_text(root: Path = ROOT) -> str:
    return "".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.relative_to(root).as_posix() + "\n" for p in inventory(root))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true", help="Explicitly regenerate release hashes after reviewing intentional changes")
    args = parser.parse_args()
    errors = structural_errors()
    if errors:
        print("RELEASE_GATE_FAILED\n" + "\n".join(errors), file=sys.stderr)
        return 2
    expected = manifest_text()
    manifest = ROOT / "MANIFEST.sha256"
    if args.write_manifest:
        manifest.write_text(expected, encoding="utf-8", newline="\n")
        print("MANIFEST_WRITTEN — validate again before release")
    elif not manifest.exists() or manifest.read_text(encoding="utf-8") != expected:
        print("RELEASE_GATE_FAILED: missing/changed/untracked release file; review changes before regenerating manifest", file=sys.stderr)
        return 2
    else:
        print("LITE_RELEASE_GATE_PASSED — static checks and integrity only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())