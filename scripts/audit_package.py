#!/usr/bin/env python3
"""Audit the deployable Coding Discipline skill package.

Checks the package carrier, links, frontmatter, executable scripts, test presence, and
basic secret-like payloads. It intentionally does not validate provenance or prove
that prose rules are semantically correct.
"""

from __future__ import annotations

import argparse
import re
import stat
import sys
from pathlib import Path

MAX_TEXT_BYTES = 2 * 1024 * 1024
REQUIRED_FILES = {
    "SKILL.md",
    "README.md",
    "DESIGN_RATIONALE.md",
    "LICENSE",
    "references/exploration_and_planning.md",
    "references/tdd_debugging_and_verification.md",
    "references/anti_slop_and_failure_modes.md",
    "references/refactoring_review_and_security.md",
    "references/harness_hooks_and_long_horizon.md",
    "references/contrastive_behavior_anchors.md",
    "scripts/audit_package.py",
    "scripts/guard_diff.py",
    "scripts/validate_evidence.py",
    "tests/test_scripts.py",
    ".github/workflows/validate.yml",
    "SECURITY.md",
    "CONTRIBUTING.md",
}
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
PATH_LITERAL_RE = re.compile(r"`((?:references|scripts)/[^`\s]+)`")
CITATION_RE = re.compile(r"\*\([^\n]*[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\s+·\s+[^)]+\)\*")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[opusr]_[A-Za-z0-9]{20,}\b"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "generic assigned secret": re.compile(r"(?i)\b(?:api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"\n]{12,}['\"]"),
}


def text_files(root: Path) -> list[Path]:
    allowed = {".md", ".py", ".json", ".toml", ".yml", ".yaml", ".txt"}
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file() and ".git" not in path.relative_to(root).parts and path.suffix.lower() in allowed
    )


def read_text(path: Path) -> str:
    data = path.read_bytes()
    if len(data) > MAX_TEXT_BYTES:
        raise ValueError(f"{path}: text file exceeds {MAX_TEXT_BYTES} bytes")
    return data.decode("utf-8")


def audit(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    for required in sorted(REQUIRED_FILES - actual):
        errors.append(f"missing required file: {required}")

    skill_path = root / "SKILL.md"
    if skill_path.is_file():
        try:
            skill = read_text(skill_path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(str(exc))
            skill = ""
        frontmatter = re.match(r"\A---\n(.*?)\n---\n", skill, flags=re.S)
        if not frontmatter:
            errors.append("SKILL.md must begin with YAML frontmatter")
        else:
            block = frontmatter.group(1)
            names = re.findall(r"(?m)^name:\s*(.+)$", block)
            descriptions = re.findall(r"(?m)^description:\s*(.+)$", block)
            if names != ["coding-discipline"]:
                errors.append("SKILL.md frontmatter must contain exactly `name: coding-discipline`")
            if len(descriptions) != 1 or not descriptions[0].strip():
                errors.append("SKILL.md frontmatter requires one non-empty description")
        line_count = len(skill.splitlines())
        if line_count > 200:
            errors.append(f"SKILL.md has {line_count} lines; limit is 200")

    for path in text_files(root):
        relative = path.relative_to(root).as_posix()
        try:
            content = read_text(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if "\x00" in content:
            errors.append(f"{relative}: contains a NUL byte")
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                errors.append(f"{relative}: possible {label}")
        if relative == "SKILL.md" or relative.startswith("references/"):
            if "## " in content and not CITATION_RE.search(content):
                errors.append(f"{relative}: no corpus-style `owner/repo · path` citation found")
        if path.suffix.lower() == ".md":
            targets = [match.group(1) for match in LINK_RE.finditer(content)]
            literal_targets = [match.group(1) for match in PATH_LITERAL_RE.finditer(content)]
            for literal in literal_targets:
                if "*" not in literal and literal not in targets:
                    targets.append(literal)
            for target in targets:
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                clean = target.split("#", 1)[0]
                if not clean:
                    continue
                if target.startswith(("./", "../")):
                    candidate = (path.parent / clean).resolve()
                elif target.startswith(("references/", "scripts/")):
                    candidate = (root / clean).resolve()
                else:
                    candidate = (path.parent / clean).resolve()
                try:
                    candidate.relative_to(root.resolve())
                except ValueError:
                    errors.append(f"{relative}: reference escapes package root: {target}")
                    continue
                if not candidate.exists():
                    errors.append(f"{relative}: missing local reference: {target}")

    for path in sorted((root / "scripts").glob("*.py")) if (root / "scripts").is_dir() else []:
        mode = path.stat().st_mode
        if not (mode & stat.S_IXUSR):
            errors.append(f"{path.relative_to(root)} is not executable")
        first = path.read_text(encoding="utf-8").splitlines()[:1]
        if first != ["#!/usr/bin/env python3"]:
            errors.append(f"{path.relative_to(root)} lacks the expected python3 shebang")

    empty_dirs = [
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_dir() and ".git" not in path.relative_to(root).parts and not any(path.iterdir())
    ]
    if empty_dirs:
        warnings.append("empty directories: " + ", ".join(sorted(empty_dirs)))
    generated = [
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if ".git" not in path.relative_to(root).parts
        and (path.name == "__pycache__" or (path.is_file() and path.suffix in {".pyc", ".pyo"}))
    ]
    if generated:
        warnings.append("generated Python cache entries present (exclude from releases): " + ", ".join(generated))
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"audit_package: not a directory: {root}", file=sys.stderr)
        return 2
    errors, warnings = audit(root)
    for warning in warnings:
        print(f"WARN {warning}")
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print(f"audit_package: FAIL ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1
    print(f"audit_package: PASS ({len(REQUIRED_FILES)} required files, {len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
