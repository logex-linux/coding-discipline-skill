# Refactoring, Review, And Security

Load this reference for refactors, review requests, compatibility work, auth/data
boundaries, or performance-sensitive changes. Review behavior and risk before style.
The source paths are corpus-supplied provenance claims, not locally rechecked raw
files because `03_参考原件/` is absent.

## Refactor Boundary

State which lines change behavior and which only improve structure. If both are
needed, make the steps or commits independently reviewable and give each its own
check. Declare the blast radius: local, module, public interface, data, or deploy.
Do not hide a behavior change inside a cleanup diff. *(obra/superpowers ·
skills/receiving-code-review/SKILL.md; quanru/code-review-skill · SKILL.md;
AlexZio00/sovereign-skills · skills/ssot-audit/SKILL.md)*

Prefer the smallest change that satisfies the named requirement. An abstraction is
justified by repeated behavior, a stable boundary, or a measured reduction in
duplication/complexity; do not build a framework for one or two call sites. Record
why extraction is cheaper than duplication and which test protects the boundary.
*(quanru/code-review-skill · SKILL.md; Hexatonic-Lab/engineering-excellence ·
SKILL.md)*

## Review Order

1. Correctness: does the change satisfy the requested behavior and preserve stated
   invariants?
2. Security: can an attacker bypass authorization, validation, isolation, or
   encoding assumptions?
3. Compatibility/data: do callers, schemas, migrations, generated files, and
   rollback paths still work?
4. Performance: did complexity, I/O, allocation, concurrency, or cache behavior
   change on a real path?
5. Maintainability: only after the above, assess names, duplication, and style.

Every finding names a concrete file/line or behavior, impact, confidence, and a
minimal fix or required evidence. “Looks fine” is not a finding or an approval.
*(h4ni0/pr-review · SKILL.md; svyatov/supermatt · SKILL.md;
obra/superpowers · skills/requesting-code-review/SKILL.md)*

## Security Pairing

For a security requirement, compare the same scenario in two versions:

```text
Requirement: ...
VULNERABLE: input/actor/context, observed result, why it violates the requirement.
SAFE: same input/actor/context, observed result, why the control holds.
Bypasses tried: encoding, alternate route, missing field, boundary value, replay,
               privilege change, concurrency or parser variation as applicable.
False positives: plausible alerts that the evidence rules out.
```

Do not call a happy-path authorization test a security audit. Include negative and
boundary cases appropriate to the boundary, and state what was not tested.
*(ersinkoc/security-check · SKILL.md; anthropics/claude-code-security-review ·
commands/security-review.md; ThirdKeyAI/Symbiont · SKILL.md)*

## Adversarial Diff Review

Trace the changed path end to end and record findings by behavior, not taste:

- **Boundaries:** empty/null/maximum values, malformed input, alternate encodings/routes, partial responses, and version skew.
- **State and concurrency:** single owner/source of truth, stale cache/epoch, duplicate or lost handoff, ordering, replay/idempotency, atomicity, cancellation, and partial failure.
- **Resources:** files/sockets/locks/processes/subscriptions are released on success, error, timeout, and cancellation; retries cannot multiply leaks.
- **Security:** authentication versus authorization, tenant/user isolation, validation before side effects, secret/private-data egress, command/path construction, and fail-open behavior.
- **Compatibility/data:** public callers, serialized formats, generated artifacts, migrations, rollback, flags, and removal of obsolete references.
- **Performance:** complexity and I/O on a real path, bounded queues/retries, cache invalidation, and measured workload rather than code-shape intuition.

For each material finding write: `path/behavior -> triggering input/state -> impact -> confidence -> minimal fix or missing evidence`. Name untested dimensions instead of silently passing them. *(eliasforge/fable-agent-orchestration · skills/adversarial-reviewer/SKILL.md; Faithree/code-review-skill · RULES.md; trailofbits/skills · plugins/differential-review/skills/differential-review/SKILL.md)*

## Compatibility And Performance

Trace public callers, serialized formats, feature flags, retries, and generated
artifacts before changing a contract. If compatibility is intentionally broken,
name the migration and rollback evidence. For performance, establish a baseline,
measure the changed path, and report workload/limits; do not infer improvement from
code shape. *(stainless-code/codemap · README.md; drafael/coding-harness ·
SKILL.md; BaseInfinity/claude-sdlc-harness · SKILL.md)*

## Carrier Review

When reviewing a skill, hook, or script itself, inspect YAML parsing, staged loaders,
shell quoting, path handling, environment inheritance, temporary files, command
construction, and permission boundaries. A tool that enforces a rule can introduce
the vulnerability it claims to prevent. *(oguzhantopgul/skill-security-reviewer ·
SKILL.md; github/gh-aw-firewall · README.md)*

## Review Stop Conditions

Mark the review `BLOCKED` or `UNVERIFIED` when the diff, baseline, required runtime,
or source of truth is unavailable. Do not lower a finding because the patch is
convenient, the author is confident, or another agent reported success. *(DollarDill/
beads-superpowers · SKILL.md; asklokesh/claudeskill-loki-mode · SKILL.md)*
