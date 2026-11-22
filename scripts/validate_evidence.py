#!/usr/bin/env python3
"""Validate a machine-readable evidence receipt.

Exit codes: 0 = internally consistent receipt, 1 = invalid/inconsistent receipt,
2 = unreadable input. This validates evidence shape and gate semantics, not whether a
command really ran or whether its output proves semantic correctness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

STATUSES = {"PASS", "BLOCKED", "UNVERIFIED", "DEGRADED"}
CHECK_STATES = {"passed", "failed", "not_run"}
MAX_RECEIPT_BYTES = 5 * 1024 * 1024
SHELL_META_RE = re.compile(r"[;&|><`\n]|\$\(")


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["receipt must be a JSON object"]

    status = data.get("status")
    if status not in STATUSES:
        errors.append(f"status must be one of {sorted(STATUSES)}")

    facts = data.get("facts")
    if not isinstance(facts, list):
        errors.append("facts must be an array")
        facts = []
    for index, fact in enumerate(facts):
        prefix = f"facts[{index}]"
        if not isinstance(fact, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not is_nonempty_string(fact.get("command")):
            errors.append(f"{prefix}.command must be a non-empty string")
        exit_code = fact.get("exit_code")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            errors.append(f"{prefix}.exit_code must be an integer")
        if not is_nonempty_string(fact.get("output")):
            errors.append(f"{prefix}.output must summarize the observed output")
        artifacts = fact.get("artifacts", [])
        if not isinstance(artifacts, list) or not all(is_nonempty_string(item) for item in artifacts):
            errors.append(f"{prefix}.artifacts must be an array of non-empty strings")

    if not is_nonempty_string(data.get("assessment")):
        errors.append("assessment must be a non-empty string and separate from facts")

    checks = data.get("checks")
    if not isinstance(checks, list) or not checks:
        errors.append("checks must be a non-empty array")
        checks = []
    for index, check in enumerate(checks):
        prefix = f"checks[{index}]"
        if not isinstance(check, dict):
            errors.append(f"{prefix} must be an object")
            continue
        if not is_nonempty_string(check.get("name")):
            errors.append(f"{prefix}.name must be a non-empty string")
        if check.get("state") not in CHECK_STATES:
            errors.append(f"{prefix}.state must be one of {sorted(CHECK_STATES)}")
        if not is_nonempty_string(check.get("evidence")):
            errors.append(f"{prefix}.evidence must identify output, artifact, or the reason not run")

    for key in ("not_run", "changed_files", "residual_risks"):
        value = data.get(key)
        if not isinstance(value, list) or not all(is_nonempty_string(item) for item in value):
            errors.append(f"{key} must be an array of non-empty strings")

    has_failed = any(isinstance(item, dict) and item.get("state") == "failed" for item in checks)
    has_not_run = any(isinstance(item, dict) and item.get("state") == "not_run" for item in checks)
    not_run = data.get("not_run") if isinstance(data.get("not_run"), list) else []
    nonzero_fact = any(
        isinstance(item, dict)
        and isinstance(item.get("exit_code"), int)
        and not isinstance(item.get("exit_code"), bool)
        and item["exit_code"] != 0
        for item in facts
    )

    if status == "PASS":
        if not facts:
            errors.append("PASS requires at least one fresh command fact")
        if has_failed or has_not_run or not_run:
            errors.append("PASS cannot contain failed/not_run checks or a non-empty not_run list")
        if nonzero_fact:
            errors.append("PASS cannot cite a non-zero command exit as completion evidence")
    elif status == "BLOCKED":
        if not has_not_run and not not_run:
            errors.append("BLOCKED must name at least one unavailable check/input")
    elif status == "UNVERIFIED":
        if not has_not_run and not not_run and facts:
            errors.append("UNVERIFIED must name missing/stale evidence or an unrun check")
    elif status == "DEGRADED":
        if not facts:
            errors.append("DEGRADED requires the narrower check that actually ran")
        if not data.get("residual_risks"):
            errors.append("DEGRADED must state what the narrower evidence cannot cover")

    return errors


def load_receipt(path: Path) -> Any:
    if path.stat().st_size > MAX_RECEIPT_BYTES:
        raise ValueError(f"receipt exceeds {MAX_RECEIPT_BYTES} bytes")
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    parser.add_argument("--run", action="store_true", help="run fact commands after explicit human approval")
    args = parser.parse_args()
    try:
        data = load_receipt(args.receipt)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"validate_evidence: {exc}", file=sys.stderr)
        return 2

    if args.run:
        facts = data.get("facts", []) if isinstance(data, dict) else []
        for index, fact in enumerate(facts):
            command = fact.get("command", "") if isinstance(fact, dict) else ""
            if SHELL_META_RE.search(command):
                print(f"validate_evidence: facts[{index}].command contains shell metacharacters; refusing replay", file=sys.stderr)
                return 2
        print("validate_evidence: --run is intentionally unsupported; replay commands explicitly in the target repository", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        print(f"validate_evidence: invalid ({len(errors)} error(s))")
        return 1
    print(f"validate_evidence: valid {data['status']} receipt (shape/semantics only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
