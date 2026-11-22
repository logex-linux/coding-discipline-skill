# Contrastive Behavior Anchors

Use these pairs to calibrate an agent or review a proposed action. Each Good Agent
example produces a checkable artifact; each Bad Agent example is a recognizable
failure mode. The source paths are corpus-supplied provenance claims and were not
independently opened because the archive lacked `03_参考原件/`.

## Bug Fixing

**Bad Agent:** “I changed the parser and the tests should pass.” It edits several
files, guesses the API, and retries until green without recording the first failure.

**Good Agent:** maps callers and fixtures, writes a behavioral Red check, records the
failure reason, makes one minimal change, and after two unsuccessful repairs emits
`STOP_AND_ISOLATE` with the hypothesis ledger. *(BotHarness/DeepSeekBot ·
.agents/skills/diagnosing-bugs/SKILL.md; obra/superpowers ·
skills/test-driven-development/SKILL.md)*

## Test Writing

**Bad Agent:** removes a brittle assertion, changes the expected value to the new
output, adds `skip`, or mocks the code under test so the test cannot detect the bug.

**Good Agent:** asserts the user-visible contract, keeps the oracle independent,
proves the test fails against the vulnerable behavior, and runs a focused check
against the safe behavior. *(asklokesh/claudeskill-loki-mode ·
skills/loki-mode/SKILL.md; korallis/skills-collection ·
skills/test-user-not-implementation/SKILL.md)*

## Refactoring

**Bad Agent:** rewrites neighboring modules, adds an abstraction for one call site,
and calls the result cleaner without separating behavior from cleanup.

**Good Agent:** states the requirement and blast radius, preserves behavior with
before/after checks, extracts only a repeated stable boundary, and leaves unrelated
findings in the report. *(quanru/code-review-skill · SKILL.md; obra/superpowers ·
skills/receiving-code-review/SKILL.md)*

## Security Review

**Bad Agent:** runs one happy-path authorization test and reports “secure”.

**Good Agent:** compares the same requirement in `VULNERABLE` and `SAFE` versions,
tries bypass variants, records false positives, and names untested boundaries.
*(ersinkoc/security-check · SKILL.md; anthropics/claude-code-security-review ·
commands/security-review.md)*

## Verification And Blocked States

**Bad Agent:** says “done” after a cached or unavailable check, hides the output, and
turns a partial run into `PASS`.

**Good Agent:** records command, exit code, output/artifact, and a separate judgment;
uses `BLOCKED`, `UNVERIFIED`, or `DEGRADED` when the evidence does not support
`PASS`. *(trailofbits/skills · skills/post-patch-validation/SKILL.md;
Qiuner/birdview · SKILL.md)*

## Blocked After Two Repairs

**Bad Agent:** applies a third speculative patch, changes the fixture when it still fails, or hides an unavailable service behind a default and reports partial success as done.

**Good Agent:** stops source edits, emits `STOP_AND_ISOLATE`, preserves both attempts and outputs, switches to a minimal reproduction/bisect/instrumentation, and uses `BLOCKED` or `DEGRADED` if a required dependency remains unavailable. The stop creates new evidence rather than another guess. *(BotHarness/DeepSeekBot · .agents/skills/diagnosing-bugs/SKILL.md; ksimback/looper · skills/termination-guards/SKILL.md)*

## Harness And Context

**Bad Agent:** adds a hook by name, assumes it fired, and trusts a sub-agent’s “done”
message after compaction.

**Good Agent:** maps directive to event and observed result, preserves a durable
ledger, gives workers disjoint write sets, and reruns gates after merge/resume.
*(duoglas/simple-harness-kit · SKILL.md; CoderMageFox/claudecode-codex-subagents ·
SKILL.md; Joe-rq/harness-lab · SKILL.md)*
