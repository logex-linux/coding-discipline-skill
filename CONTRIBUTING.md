# Contributing

Keep changes surgical and evidence-backed.

1. State the behavior delta and non-goals.
2. Add or update a negative fixture before changing a guard.
3. Do not weaken an existing fixture to make a script pass.
4. Run:

   ```bash
   python3 scripts/audit_package.py .
   python3 -m unittest discover -s tests -v
   ```

5. Explain regex/scanner false-positive and false-negative boundaries in the relevant docstring or reference.
6. Keep `SKILL.md` below 200 lines; route stage detail into `references/`.

A scanner rule must name the concrete failure mode it blocks. Generic style preferences and framework-specific policy do not belong in the always-on constitution.
