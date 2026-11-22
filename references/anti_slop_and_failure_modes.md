# Anti-Slop And Failure Modes

Load this reference when a diff, test, retry loop, or completion claim shows signs of reward hacking. Use it as a symptom-to-action table, not as a style guide. Text scanners can flag carrier patterns; only behavioral checks and review can decide intent or correctness.

## Correction Table

| Symptom | Detect | Required correction |
|---|---|---|
| **Fake Red** | The new test errors during import/setup, never reaches the assertion, or passes before the fix. | Repair the seam/fixture first. Capture a failure caused by the requested behavior before editing production code. |
| **Oracle manipulation** | Assertions disappear; expected values, thresholds, or matchers become easier; `skip`, `only`, `xfail`, input-specific branches, `any`, or ignore directives appear. | Stop. Restore the independent contract oracle. If the requirement truly changed, record that requirement and review the test change separately. Run `python3 scripts/guard_diff.py --diff change.patch`. |
| **Circular test** | The system under test generates its own expected value, or a mock replaces the changed behavior. | Derive expectations from the contract or a separate oracle. Prove the test fails against the known-bad behavior. |
| **Silent failure** | Empty/broad catch, default fallback, `|| true`, `continue-on-error`, missing directory interpreted as clean, or failed scanner treated as no findings. | Preserve/re-raise the error, or return a documented error state. A guard that cannot run is `BLOCKED`/`UNVERIFIED`, not clean. |
| **Blind repair loop** | Patches accumulate without a written hypothesis; the same target check does not improve twice. | Emit `STOP_AND_ISOLATE`; stop source edits, record attempts/evidence, build a minimal reproduction or switch observation technique. |
| **Retry cascade** | Retry is unbounded, immediate, applied to auth/validation errors, or repeats a non-idempotent operation. | Classify retryability; require a bound, backoff+jitter, timeout budget, and idempotency protection where side effects exist. |
| **Invented interface** | A plausible API, flag, config key, or path appears without repository/docs evidence. | Search the installed version, repository, `--help`, or current vendor docs. If unavailable, mark the dependency `BLOCKED`; do not guess. |
| **Scope creep** | Unrelated formatting/refactoring/config/dependency changes ride with the requested fix. | Remove unrelated edits. Report adjacent issues as follow-ups; every changed line must trace to scope or task-created cleanup. |
| **Speculative abstraction** | A helper/framework serves one consumer, branches on `mode/kind`, or anticipates unnamed future needs. | Inline or duplicate the small behavior unless repeated real consumers share one change direction and a nameable boundary. |
| **Partial removal** | A feature is disabled but dead routes, flags, imports, docs, generated artifacts, or persisted state remain. | Either restore the feature or complete removal across references and artifacts, with migration/rollback evidence where state is involved. |
| **Environment tampering** | Tests, CI, permissions, fixtures, or config change only to make the failure disappear. | Revert the bypass; fix the candidate implementation. Treat environment/test changes as separate, explicitly authorized scope. |
| **Fake completion** | “Done/passes/fixed” relies on stale, cached, partial, unavailable, or hidden evidence. | Run a fresh post-edit check and issue an evidence receipt. Use `BLOCKED`, `UNVERIFIED`, or `DEGRADED` when warranted. |

These actions operationalize the corpus’s predictable-failure checklist, test-integrity rules, bounded debugging, and complete-execution discipline. *(OneWave-AI/claude-skills · skills/ai-coding-guardrails/SKILL.md; obra/superpowers · skills/systematic-debugging/SKILL.md; trailofbits/skills · plugins/patching-bugs/skills/prove-patch/SKILL.md; asklokesh/claudeskill-loki-mode · skills/loki-mode/SKILL.md; ariadoss/superskills · engineering-mindset/SKILL.md)*

## Two-Failed-Repairs Breaker

Count a repair as unsuccessful when the target behavioral signal stays failed, becomes a different setup failure, or produces no discriminating evidence. After two consecutive unsuccessful repairs:

```text
STOP_AND_ISOLATE
Target signal: ...
Attempt 1 / evidence / decision: ...
Attempt 2 / evidence / decision: ...
Assumptions now falsified: ...
Next observation technique: minimal reproduction | bisect | instrumentation | differential check
Missing input or architectural question: ...
```

Do not make a third speculative source patch. The stop does not mean abandon the task; it means replace patch generation with evidence generation. *(BotHarness/DeepSeekBot · .agents/skills/diagnosing-bugs/SKILL.md; serpro69/claude-toolbox · skills/verify/SKILL.md; ksimback/looper · skills/termination-guards/SKILL.md)*

## Retry Contract

Before adding or changing retries, record:

```text
Operation and side effect: ...
Retryable failures: ...
Non-retryable failures: auth | validation | deserialization | other: ...
Idempotency mechanism: key | transaction | none (why safe): ...
Max attempts / total deadline: ...
Backoff and jitter: ...
Observable terminal error: ...
```

Never retry a non-idempotent operation without an idempotency mechanism. Each nested timeout must fit inside its caller’s remaining budget. *(arbazkhan971/godmode · skills/resilience/SKILL.md)*

## Diff Self-Review

Before closing, inspect the final diff and answer:

1. Can the test fail if the old bug returns, or would its mocks/fixtures still pass?
2. Did any expected value, assertion, threshold, skip/focus marker, type rule, or CI gate change? If yes, where is the independent requirement?
3. Did a catch, fallback, retry, or status conversion hide a failure?
4. Does every changed line map to the requested behavior, a required test, or cleanup caused by this task?
5. Did the implementation create a second state owner, parser, approval path, or compatibility branch?
6. Did deletion/removal leave references, generated files, migrations, docs, or callers behind?
7. Is the completion claim backed by fresh post-final-edit evidence?

A clean scanner result answers none of these semantic questions; it only means the listed textual patterns were not detected.
