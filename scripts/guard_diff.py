#!/usr/bin/env python3
"""Flag diff patterns that commonly manufacture a false green result.

Exit codes: 0 = no findings, 1 = review/block findings, 2 = invalid input.
The scanner is intentionally conservative: findings require human review and do not
prove intent or semantic incorrectness.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

MAX_DIFF_BYTES = 20 * 1024 * 1024
HUNK_RE = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
TEST_PATH_RE = re.compile(r"(^|/)(tests?|__tests__|spec)(/|$)|(?:^|[._-])(test|spec)\.", re.I)
CODE_SUFFIXES = {".c", ".cc", ".cpp", ".cs", ".go", ".java", ".js", ".jsx", ".kt", ".php", ".py", ".rb", ".rs", ".swift", ".ts", ".tsx"}


@dataclass(frozen=True)
class ChangedLine:
    path: str
    hunk: int
    line: int
    text: str
    added: bool


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    path: str
    line: int | None
    message: str


def normalized_path(raw: str) -> str:
    value = raw.split("\t", 1)[0].strip()
    if value in {"/dev/null", ""}:
        return value
    return value[2:] if value.startswith(("a/", "b/")) else value


def parse_diff(text: str) -> tuple[list[ChangedLine], set[str]]:
    lines: list[ChangedLine] = []
    deleted: set[str] = set()
    old_path = new_path = ""
    old_line = new_line = 0
    hunk = 0

    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            parts = raw.split()
            old_path = normalized_path(parts[2]) if len(parts) > 2 else ""
            new_path = normalized_path(parts[3]) if len(parts) > 3 else ""
            continue
        if raw.startswith("--- "):
            old_path = normalized_path(raw[4:])
            continue
        if raw.startswith("+++ "):
            new_path = normalized_path(raw[4:])
            if new_path == "/dev/null" and old_path:
                deleted.add(old_path)
            continue
        match = HUNK_RE.match(raw)
        if match:
            hunk += 1
            old_line, new_line = int(match.group(1)), int(match.group(2))
            continue
        if not hunk:
            continue
        path = new_path if new_path != "/dev/null" else old_path
        if raw.startswith("+") and not raw.startswith("+++"):
            lines.append(ChangedLine(path, hunk, new_line, raw[1:], True))
            new_line += 1
        elif raw.startswith("-") and not raw.startswith("---"):
            lines.append(ChangedLine(path, hunk, old_line, raw[1:], False))
            old_line += 1
        elif raw.startswith(" "):
            old_line += 1
            new_line += 1
    return lines, deleted


def is_test_path(path: str) -> bool:
    return bool(TEST_PATH_RE.search(path))


def is_code_path(path: str) -> bool:
    return Path(path).suffix.lower() in CODE_SUFFIXES


def scan(text: str) -> list[Finding]:
    changed, deleted = parse_diff(text)
    findings: list[Finding] = []

    def add(code: str, severity: str, item: ChangedLine, message: str) -> None:
        findings.append(Finding(code, severity, item.path, item.line, message))

    assertion_re = re.compile(r"\b(assert|expect\s*\(|should\.|assert[A-Z]\w*\s*\()")
    skip_re = re.compile(r"(?:\b(?:it|test|describe)\.(?:skip|only)\b|\b(?:xit|xdescribe|xtest)\s*\(|@pytest\.mark\.(?:skip|xfail)|pytest\.skip\s*\()")
    trivial_assert_re = re.compile(r"(?:\bassert\s+True\b|expect\s*\(\s*true\s*\)\s*\.toBe\s*\(\s*true\s*\))", re.I)
    ignore_re = re.compile(r"(?:@ts-(?:ignore|nocheck)|#\s*type:\s*ignore|#\s*noqa\b|eslint-disable|noinspection)", re.I)
    any_re = re.compile(r"(?:\bas\s+any\b|:\s*any\b|<any>)")
    bypass_re = re.compile(r"(?:\|\|\s*true\b|--no-verify\b|continue-on-error\s*:\s*true|allow_failure\s*:\s*true)", re.I)
    broad_catch_re = re.compile(r"(?:except\s+(?:Exception|BaseException)\b|catch\s*\([^)]*\))")
    silent_inline_re = re.compile(r"(?:except[^:]*:\s*pass\b|catch\s*\([^)]*\)\s*\{\s*\})")

    for item in changed:
        stripped = item.text.strip()
        if item.added:
            if skip_re.search(stripped):
                add("TEST_DISABLED", "block", item, "new skip/focus marker can hide failing tests")
            if trivial_assert_re.search(stripped):
                add("TRIVIAL_ASSERTION", "block", item, "assertion is true regardless of behavior")
            if is_code_path(item.path) and ignore_re.search(stripped):
                add("TYPE_CHECK_BYPASS", "block", item, "new ignore directive bypasses a deterministic check")
            elif is_code_path(item.path) and any_re.search(stripped):
                add("TYPE_WIDENING", "review", item, "new `any` may silence the contract being tested")
            if silent_inline_re.search(stripped):
                add("SILENT_CATCH", "block", item, "catch/except discards the failure")
            elif broad_catch_re.search(stripped):
                add("BROAD_CATCH", "review", item, "broad catch requires an explicit preserve-or-report path")
            if bypass_re.search(stripped):
                add("GATE_BYPASS", "block", item, "new command/config can turn a failed gate into success")
        elif assertion_re.search(stripped):
            severity = "block" if is_test_path(item.path) else "review"
            code = "ORACLE_REMOVED" if is_test_path(item.path) else "INVARIANT_REMOVED"
            add(code, severity, item, "removed assertion may weaken the behavior oracle")

    grouped: dict[tuple[str, int], list[ChangedLine]] = {}
    for item in changed:
        if item.added:
            grouped.setdefault((item.path, item.hunk), []).append(item)
    for items in grouped.values():
        for index, item in enumerate(items):
            if re.match(r"^except\b[^:]*:\s*$", item.text.strip()):
                following = [line.text.strip() for line in items[index + 1 : index + 4] if line.text.strip()]
                if following and following[0] in {"pass", "return", "return None"}:
                    add("SILENT_CATCH", "block", following_item(items, index), "except block immediately discards the failure")

    for path in sorted(deleted):
        if is_test_path(path):
            findings.append(Finding("TEST_FILE_DELETED", "block", path, None, "deleted test file reduces the oracle surface"))

    unique: dict[tuple[str, str, str, int | None], Finding] = {}
    for finding in findings:
        unique[(finding.code, finding.severity, finding.path, finding.line)] = finding
    return sorted(unique.values(), key=lambda item: (item.path, item.line or 0, item.code))


def following_item(items: list[ChangedLine], index: int) -> ChangedLine:
    for item in items[index + 1 : index + 4]:
        if item.text.strip():
            return item
    return items[index]


def read_diff(path: str | None) -> str:
    if path:
        data = Path(path).read_bytes()
    else:
        data = sys.stdin.buffer.read(MAX_DIFF_BYTES + 1)
    if len(data) > MAX_DIFF_BYTES:
        raise ValueError(f"diff exceeds {MAX_DIFF_BYTES} bytes")
    return data.decode("utf-8", errors="replace")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diff", help="unified diff file; omit to read stdin")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()
    try:
        findings = scan(read_diff(args.diff))
    except (OSError, ValueError) as exc:
        print(f"guard_diff: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps({"status": "findings" if findings else "clean", "findings": [asdict(item) for item in findings]}, indent=2))
    elif findings:
        for item in findings:
            location = f"{item.path}:{item.line}" if item.line is not None else item.path
            print(f"{item.severity.upper()} {item.code} {location} — {item.message}")
        print(f"guard_diff: {len(findings)} finding(s); review before claiming PASS")
    else:
        print("guard_diff: clean (no detectable oracle/gate bypass patterns)")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
