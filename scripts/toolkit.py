#!/usr/bin/env python3
"""Small offline CLI. Run --help for commands; it does not call a model API."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from core import (InputError, config, load_json, make_plan, validate_plan, render_report,
                  save_text, json_text, make_utm, rsa_check)
import platform_rules


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=config()["title"] + " — offline only")
    sub = parser.add_subparsers(dest="command", required=True)
    plan = sub.add_parser("plan", help="Create deterministic starter plan + Markdown + checks")
    plan.add_argument("brief")
    plan.add_argument("--out-dir", required=True)
    validate = sub.add_parser("validate", help="Check local plan structure, never live eligibility")
    validate.add_argument("plan")
    render = sub.add_parser("render", help="Validate and render an edited plan")
    render.add_argument("plan")
    render.add_argument("--out", required=True)
    utm = sub.add_parser("utm", help="Create URL parameters locally; does not fetch the URL")
    utm.add_argument("url")
    utm.add_argument("--campaign", required=True)
    utm.add_argument("--content")
    if config()["id"] == "gooads-skill-lite":
        check = sub.add_parser("check-copy", help="Check RSA counts and conservative local text widths")
        check.add_argument("json_file")
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            output = Path(args.out_dir)
            targets = [output / name for name in ("plan.json", "report.md", "validation.json")]
            if any(p.exists() or p.is_symlink() for p in targets):
                raise InputError("Output already exists; choose another --out-dir")
            value = make_plan(load_json(args.brief), platform_rules.build)
            checks = validate_plan(value, platform_rules.validate)
            report = render_report(value, checks)
            for target, text in zip(targets, (json_text(value), report, json_text(checks))):
                save_text(target, text)
            print(json_text({"status": "PLAN_READY", "scope": "local_structure_only", "files": [str(p) for p in targets]}), end="")
        elif args.command in {"validate", "render"}:
            value = load_json(args.plan)
            checks = validate_plan(value, platform_rules.validate)
            if args.command == "render":
                save_text(args.out, render_report(value, checks))
            print(json_text(checks), end="")
        elif args.command == "utm":
            print(make_utm(args.url, args.campaign, args.content))
        elif args.command == "check-copy":
            result = rsa_check(load_json(args.json_file))
            print(json_text(result), end="")
            return 0 if result["valid"] else 2
        return 0
    except (InputError, OSError, UnicodeError) as exc:
        message = str(exc) if isinstance(exc, InputError) else f"Local file operation failed ({type(exc).__name__})"
        print("ERROR: " + message, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
