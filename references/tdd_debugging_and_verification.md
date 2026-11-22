# TDD, Debugging, And Verification

Load this reference for new behavior, bugs, failing checks, or completion claims.
The goal is an evidence chain another engineer can replay. The citations are
corpus-supplied; the raw source mirror referenced by the corpus was not included.

## Behavioral Red

The first failing check must exercise the requested behavior and fail for the
expected reason. A compile error, missing import, malformed fixture, or test that
never reaches the assertion is not Red. Capture:

```text
RED command: ...
exit code: ...
observed output/artifact: ...
expected failure reason: ...
why this distinguishes the bug from a broken test: ...
```

If the check is not behavioral, stop implementation and repair the test, fixture,
or harness first. *(BotHarness/DeepSeekBot · .agents/skills/diagnosing-bugs/SKILL.md;
obra/superpowers · skills/test-driven-development/SKILL.md; nizos/tdd-guard · README.md)*

## Debugging Ledger

Use one hypothesis at a time:

```text
Observation: directly observed fact.
Hypothesis: one causal explanation.
Prediction: result that should occur if true.
Isolation: smallest reproduction or variable removed.
Check: command or experiment.
Result: output and exit code.
Decision: confirmed | falsified | inconclusive.
```

Two consecutive repair attempts that do not improve the target check trigger
`STOP_AND_ISOLATE`. Do not add a third speculative patch. Preserve the attempted
diffs or summaries, commands, outputs, and the missing input needed to continue.
*(BotHarness/DeepSeekBot · .agents/skills/diagnosing-bugs/SKILL.md;
serpro69/claude-toolbox · skills/verify/SKILL.md; ksimback/looper ·
skills/termination-guards/SKILL.md)*

## Test Oracle Integrity

The test must describe the user or system contract, not mirror the implementation.
Block or escalate these diff patterns:

- removed or commented assertions;
- weaker matchers, lower thresholds, or changed expected values without a separate
  requirement record;
- new `skip`, `only`, `pending`, input-specific pass branches, `any`, or ignore
  directives used to silence the failure;
- mocks/fakes that replace the changed behavior and cannot fail if the real defect
  returns;
- a test that passes against both a vulnerable and a safe revision.

Run `scripts/guard_diff.py` for detectable patterns, then perform semantic review
for cases a text scanner cannot see. *(asklokesh/claudeskill-loki-mode ·
skills/loki-mode/SKILL.md; korallis/skills-collection ·
skills/test-user-not-implementation/SKILL.md; vertexcover-io/harness-engineering ·
SKILL.md)*

## Evidence Contract

Every check gets one of `passed`, `failed`, or `not_run`. The overall gate gets one
of `PASS`, `BLOCKED`, `UNVERIFIED`, or `DEGRADED`:

- `PASS`: the relevant fresh checks ran and their evidence supports the claim;
- `BLOCKED`: a required input, permission, tool, or environment was unavailable;
- `UNVERIFIED`: the work may be valid, but a required check did not run or the
  evidence is stale/missing;
- `DEGRADED`: a narrower or weaker check ran; state exactly what it cannot cover.

Keep deterministic `FACTS` separate from `ASSESSMENT`:

```json
{
  "status": "PASS",
  "facts": [{"command": "...", "exit_code": 0, "output": "...", "artifacts": ["..."]}],
  "assessment": "...",
  "checks": [{"name": "unit", "state": "passed", "evidence": "..."}],
  "not_run": [],
  "changed_files": ["..."],
  "residual_risks": []
}
```

Run `python3 scripts/validate_evidence.py receipt.json`. The validator checks
required fields and status consistency; it does not execute commands, attest that
reported output is authentic, or prove semantic correctness. Replay important
commands explicitly in the target repository when independent verification is
required. *(trailofbits/skills ·
skills/post-patch-validation/SKILL.md; Qiuner/birdview · SKILL.md;
serpro69/claude-toolbox · skills/verify/SKILL.md)*

## Proportionate Verification

Start with the smallest relevant check, then add checks according to blast radius:

| Surface | Minimum evidence | Not sufficient by itself |
|---|---|---|
| Local behavior | focused test or reproducible command | lint alone |
| Types/contracts | type check or contract test | unit test that bypasses the contract |
| Security/data boundary | vulnerable/safe pair, bypass variants, negative cases | happy-path test |
| Integration/deployment | integration/e2e plus generated artifact freshness | green e2e as proof of all coverage |
| Refactor | before/after behavior checks and diff review | formatting success |

When a check is unavailable, record why and use the correct degraded state. Never
convert a missing test into an implementation claim. Mutation sampling of three to
five critical behaviors is useful when the harness supports it, but “not sampled”
must remain visible. *(vertexcover-io/harness-engineering · SKILL.md;
AgnesAI-Labs/agnes-harness · SKILL.md; serpro69/claude-toolbox · SKILL.md)*

## Freshness

Evidence is fresh only when the command ran after the final relevant edit and the
receipt names the resulting artifact, output, or exit code. A cached prior green
result is not current proof. *(serpro69/claude-toolbox · SKILL.md;
cozytab/fable5-mode · SKILL.md)*
