#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str) -> ModuleType:
    path = ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class GuardDiffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guard = load_script("guard_diff")

    def test_clean_implementation_diff_passes(self) -> None:
        diff = """diff --git a/src/calc.py b/src/calc.py
--- a/src/calc.py
+++ b/src/calc.py
@@ -1,2 +1,2 @@
-def total(a, b): return a - b
+def total(a, b): return a + b
"""
        self.assertEqual([], self.guard.scan(diff))

    def test_removed_assertion_and_skip_are_blocked(self) -> None:
        diff = """diff --git a/tests/test_calc.py b/tests/test_calc.py
--- a/tests/test_calc.py
+++ b/tests/test_calc.py
@@ -1,3 +1,3 @@
-def test_total():
-    assert total(2, 3) == 5
+@pytest.mark.skip(reason="later")
+def test_total(): pass
"""
        codes = {item.code for item in self.guard.scan(diff)}
        self.assertIn("ORACLE_REMOVED", codes)
        self.assertIn("TEST_DISABLED", codes)

    def test_type_ignore_and_gate_bypass_are_detected(self) -> None:
        diff = """diff --git a/src/value.ts b/src/value.ts
--- a/src/value.ts
+++ b/src/value.ts
@@ -1 +1,4 @@
 export const value = input;
+// @ts-ignore
+export const unsafe: any = input;
+runChecks() || true;
"""
        codes = {item.code for item in self.guard.scan(diff)}
        self.assertTrue({"TYPE_CHECK_BYPASS", "TYPE_WIDENING", "GATE_BYPASS"}.issubset(codes))

    def test_deleted_test_file_is_blocked(self) -> None:
        diff = """diff --git a/tests/test_old.py b/tests/test_old.py
deleted file mode 100644
--- a/tests/test_old.py
+++ /dev/null
@@ -1 +0,0 @@
-assert old_behavior()
"""
        codes = {item.code for item in self.guard.scan(diff)}
        self.assertIn("TEST_FILE_DELETED", codes)


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_script("validate_evidence")

    def valid_receipt(self) -> dict:
        return {
            "status": "PASS",
            "facts": [{"command": "python3 -m unittest", "exit_code": 0, "output": "4 tests passed", "artifacts": []}],
            "assessment": "The focused regression suite supports the scoped claim.",
            "checks": [{"name": "unit", "state": "passed", "evidence": "4 tests passed"}],
            "not_run": [],
            "changed_files": ["src/calc.py", "tests/test_calc.py"],
            "residual_risks": [],
        }

    def test_valid_pass_receipt(self) -> None:
        self.assertEqual([], self.validator.validate(self.valid_receipt()))

    def test_pass_with_not_run_is_rejected(self) -> None:
        receipt = self.valid_receipt()
        receipt["checks"].append({"name": "integration", "state": "not_run", "evidence": "service unavailable"})
        receipt["not_run"] = ["integration: service unavailable"]
        errors = self.validator.validate(receipt)
        self.assertTrue(any("PASS cannot" in error for error in errors))

    def test_degraded_requires_scope_limit(self) -> None:
        receipt = self.valid_receipt()
        receipt["status"] = "DEGRADED"
        errors = self.validator.validate(receipt)
        self.assertTrue(any("DEGRADED" in error for error in errors))

    def test_blocked_requires_missing_input(self) -> None:
        receipt = self.valid_receipt()
        receipt["status"] = "BLOCKED"
        errors = self.validator.validate(receipt)
        self.assertTrue(any("BLOCKED" in error for error in errors))


class PackageAuditTests(unittest.TestCase):
    def test_package_audit_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            clean_root = Path(directory) / "coding-discipline"
            shutil.copytree(ROOT, clean_root, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))
            result = subprocess.run(
                ["python3", str(clean_root / "scripts" / "audit_package.py"), str(clean_root)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertNotIn("WARN", result.stdout)

    def test_missing_required_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text("---\nname: coding-discipline\ndescription: test\n---\n", encoding="utf-8")
            result = subprocess.run(
                ["python3", str(ROOT / "scripts" / "audit_package.py"), str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(1, result.returncode)
        self.assertIn("missing required file", result.stdout)


if __name__ == "__main__":
    unittest.main()
