---
name: coding-discipline
description: A progressive-disclosure engineering skill for coding agents that turns repository work into scoped, evidence-backed changes and blocks common test, debugging, verification, and context-management pathologies.
---

# Coding Discipline

This is a router and a small constitution, not a software textbook. Load only the
reference named by the current stage. Use the scripts when a rule can be checked
mechanically. The corpus citations below are provenance claims supplied by the
uploaded corpus; the expected `03_参考原件/` raw mirror was absent, so they are not
independent local verification.

## Core Engineering Constitution

1. **Read before writing.** Inspect the target, its imports/callers, relevant tests,
   configuration, and the nearest history before editing; if the required context
   is unavailable, mark the work `BLOCKED`. This prevents filename-based guesses.
   *(obra/superpowers · skills/writing-plans/SKILL.md; stainless-code/codemap · README.md)*
2. **Specify the behavior.** Record scope, invariants, acceptance checks, risks,
   and explicit non-goals before a non-trivial change. A small diff is not proof of
   a small blast radius. *(AlexZio00/sovereign-skills · skills/ssot-audit/SKILL.md;
   drafael/coding-harness · skills/blast-radius/SKILL.md)*
3. **Make Red behavioral.** Before production code, add or expose a test that
   fails for the requested behavior, not because of a missing import, syntax error,
   or broken fixture. *(BotHarness/DeepSeekBot · .agents/skills/diagnosing-bugs/SKILL.md;
   obra/superpowers · skills/test-driven-development/SKILL.md)*
4. **Change one variable at a time.** Debug with observation, one hypothesis, a
   prediction, a minimal reproduction or isolation, and a falsification/confirmation
   check. After two consecutive unsuccessful repairs, stop guessing and isolate.
   *(BotHarness/DeepSeekBot · .agents/skills/diagnosing-bugs/SKILL.md;
   serpro69/claude-toolbox · skills/verify/SKILL.md)*
5. **Protect the oracle.** Never delete or weaken assertions, alter expected values
   to match an implementation, add input-specific passes, widen types with `any` or
   ignore directives, or replace behavior with mocks that cannot fail on a real bug.
   *(asklokesh/claudeskill-loki-mode · skills/loki-mode/SKILL.md;
   korallis/skills-collection · skills/test-user-not-implementation/SKILL.md)*
6. **Surface failure.** Do not use broad catches, silent defaults, unbounded retries,
   or “looks fine” language to convert an error into a pass. Preserve the error or
   report the degraded state. *(OneWave-AI/claude-skills · skills/anti-slop/SKILL.md;
   ksimback/looper · skills/termination-guards/SKILL.md)*
7. **Separate behavior from cleanup.** Declare the blast radius, keep refactoring
   and behavior changes distinguishable, and clean only changes made for this task.
   *(obra/superpowers · skills/receiving-code-review/SKILL.md;
   quanru/code-review-skill · SKILL.md)*
8. **Completion is evidence.** A claim of completion requires fresh commands, exit
   codes, relevant output or artifacts, and separate `FACTS` from `ASSESSMENT`.
   Otherwise report `UNVERIFIED`; never silently downgrade `DEGRADED` to `PASS`.
   *(trailofbits/skills · skills/post-patch-validation/SKILL.md;
   Qiuner/birdview · skills/coverage-honesty/SKILL.md)*

## Red Lines For LLM Pathologies

- **Hallucinated API:** do not invent an interface, option, file, or convention;
  search the repository/docs or mark the dependency `BLOCKED`.
- **Test/result manipulation:** any assertion deletion/weakening, expected-value
  edit without an independent requirement, skip/focus addition, or mock-only test
  is a review failure. Run `python3 scripts/guard_diff.py --diff change.patch`.
- **Silent failure:** a catch must either re-raise, add context and preserve the
  failure, or explicitly return a documented error state. Run the guard on the diff.
- **Blind retry loop:** after two failed repairs, emit `STOP_AND_ISOLATE` with the
  hypotheses, commands, outputs, and missing input.
- **Overengineering:** no speculative abstraction, unrelated cleanup, dependency,
  compatibility layer, or broad rewrite without a named requirement and blast radius.
- **Fake completion:** no “fixed”, “passes”, or “done” without a current evidence
  receipt. A missing check is `not_run`; an unavailable check is `BLOCKED` or
  `DEGRADED`, never `PASS`.

## Surgical Execution Loop

1. **Recon:** map the request to files, callers, tests, configs, constraints, and
   non-goals; load `references/exploration_and_planning.md`.
2. **Plan:** state the behavior delta, invariants, risk tier, smallest edit, and
   verification commands. For bugs, state the expected Red failure.
3. **Red:** run the behavioral test and capture command, exit code, output, and
   artifact. If Red is not behavioral, stop and repair the test/fixture first.
4. **Green:** make the smallest implementation change; do not mix cleanup or
   speculative redesign. On failures use the two-attempt stop rule.
5. **Refine:** load the task-specific reference; review correctness/security before
   style and inspect the diff for scope and oracle integrity.
6. **Verify:** run the narrow check, then proportionate type/lint/integration checks;
   load `references/tdd_debugging_and_verification.md` for evidence semantics.
7. **Close:** report `PASS`, `BLOCKED`, `UNVERIFIED`, or `DEGRADED`, with `FACTS`,
   `ASSESSMENT`, changed files, residual risks, and explicit not-run checks.

## Progressive Routing Table

| Trigger | Load | Required output |
|---|---|---|
| New request, unfamiliar code, or scope change | `references/exploration_and_planning.md` | scope/spec, invariants, non-goals, blast radius |
| New behavior, bug, failing check, or uncertain root cause | `references/tdd_debugging_and_verification.md` | behavioral Red, hypothesis ledger, evidence receipt |
| Suspected test cheating, swallowed error, retry loop, scope creep, or fake completion | `references/anti_slop_and_failure_modes.md` | symptom, detectable signal, mandatory correction |
| Refactor, review, auth/data boundary, or performance concern | `references/refactoring_review_and_security.md` | behavior/cleanup split, findings, VULNERABLE/SAFE comparison |
| Hook, sub-agent, long task, context pressure, or external action | `references/harness_hooks_and_long_horizon.md` | risk tier, ledger/handoff, hook coverage, re-verification |
| Agent behavior needs calibration or review training | `references/contrastive_behavior_anchors.md` | Bad/Good contrast and violated rule |

## Mechanical Backstops

These new supplements are deterministic checks, not proof of semantic correctness:

```text
python3 scripts/audit_package.py .
python3 scripts/guard_diff.py --diff change.patch
python3 scripts/validate_evidence.py receipt.json
```

Read-only checks may run automatically. Writes/submission notify; deletion,
installation, packaging, and external sending require approval; credential transfer
and obfuscated commands are hard blocks. Batch operations over five targets and
unfamiliar objects receive one higher risk tier. Treat these as a portable policy
model: a host hook enforces them only after explicit registration and an exercised
event proves coverage. *(Myr-Aya/GouvernAI-claude-code-plugin
· skills/risk-tier/SKILL.md; inoX-Network/claude-code-safety-guard · README.md)*

## Non-Goals

This skill does not teach framework syntax, replace repository-specific policy,
prove arbitrary semantic properties with regexes, or authorize destructive/external
actions. The bundled scripts are checks, not installed host hooks. It does not treat
a green end-to-end test as complete coverage, and it does not claim the corpus
citations were independently checked when raw sources are absent.
