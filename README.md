# Coding Discipline

A progressive-disclosure engineering skill for coding agents: thin operational rules, stage-specific references, and deterministic backstops against false-green delivery.

## What This Repository Provides

- `SKILL.md`: always-on constitution, red lines, execution loop, and routing table.
- `references/`: on-demand protocols for reconnaissance, TDD/debugging, anti-slop correction, review/security, long-horizon harness work, and behavior calibration.
- `scripts/`: dependency-free checks for package shape, suspicious diff patterns, and evidence-receipt consistency.
- `tests/`: positive and negative fixtures for the scripts.
- `DESIGN_RATIONALE.md`: source boundary, retained engineering genes, deterministic limits, and A/B pressure scenarios.

The skill does **not** replace repository policy or prove semantic correctness with regexes. Its scanners produce review findings, not infallible verdicts.

## Install

Copy or symlink this directory into the skill directory used by your agent harness. The deployable root must preserve this layout:

```text
coding-discipline/
├── SKILL.md
├── references/
├── scripts/
└── tests/
```

No third-party Python packages are required. Python 3.10+ is recommended.

## Validate The Package

Run from the repository root:

```bash
python3 scripts/audit_package.py .
python3 -m unittest discover -s tests -v
```

Audit a pending patch:

```bash
git diff --cached --no-ext-diff --binary > /tmp/change.patch
python3 scripts/guard_diff.py --diff /tmp/change.patch
```

Validate an evidence receipt:

```bash
python3 scripts/validate_evidence.py receipt.json
```

A minimal valid receipt:

```json
{
  "status": "PASS",
  "facts": [
    {
      "command": "python3 -m unittest discover -s tests -v",
      "exit_code": 0,
      "output": "all tests passed",
      "artifacts": []
    }
  ],
  "assessment": "The focused suite supports the scoped claim.",
  "checks": [
    {"name": "unit", "state": "passed", "evidence": "all tests passed"}
  ],
  "not_run": [],
  "changed_files": ["src/example.py", "tests/test_example.py"],
  "residual_risks": []
}
```

`validate_evidence.py` validates internal shape and status semantics. It deliberately does not execute receipt commands or prove that the reported output is authentic.

## Status Semantics

- `PASS`: relevant fresh checks ran after the final edit and support the scoped claim.
- `BLOCKED`: a required input, permission, tool, or environment was unavailable.
- `UNVERIFIED`: required evidence is missing or stale.
- `DEGRADED`: a narrower check ran; residual coverage limits are explicit.

## License

MIT. See [LICENSE](LICENSE).
