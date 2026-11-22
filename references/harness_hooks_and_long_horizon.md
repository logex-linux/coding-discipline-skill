# Harness, Hooks, And Long-Horizon Work

Load this reference when the task spans context windows, uses sub-agents, installs
hooks, touches external systems, or needs durable progress. Prompt guidance changes
probabilities; deterministic constraints belong in scripts, tests, or hooks. These
citations are claims supplied by the corpus; raw mirrors were not included.

## Enforcement Boundary

Put judgment and sequencing in the prompt. Put non-bypassable requirements in a
deterministic backstop: command guard, diff scanner, test, CI check, or hook. Keep a
coverage matrix with `directive -> event -> registered check -> observed result`;
configured is not effective until the event is exercised. *(jack-reson8/skill-skill ·
SKILL.md; duoglas/simple-harness-kit · SKILL.md; redpanda-data/ui-harness · SKILL.md)*

Use proportional risk tiers:

| Action | Default treatment |
|---|---|
| read/search/check | automatic |
| write/edit/submit | notify and show scope |
| delete/install/package/external send | approval required |
| credential transfer or obfuscated command | hard block |

Raise one tier for five or more targets or an unfamiliar object. Do not make a hook
claim more coverage than its event and runtime can observe. *(Myr-Aya/
GouvernAI-claude-code-plugin · SKILL.md; inoX-Network/claude-code-safety-guard ·
README.md; Joe-rq/harness-lab · SKILL.md)*

## Durable Ledger

Use a small append-only ledger rather than relying on conversation memory:

```text
Objective and acceptance:
Constraints and approvals:
Known facts and source paths:
Hypotheses and failed attempts:
Changed files and ownership:
Commands/evidence/artifacts:
Open risks and next action:
```

After context compaction, re-read the ledger and re-verify the last claimed state.
Only carry forward facts with evidence; label distilled assumptions. At pressure
thresholds, name what was evicted and why. *(doncheli/don-cheli-sdd · SKILL.md;
robertguss/claude-skills · SKILL.md; Joe-rq/harness-lab · SKILL.md)*

## Delegation And Merge

Give each worker a disjoint write set and a bounded objective. Cap fan-out at the
available verification capacity; chain the remainder. Workers return paths changed,
commands run, exit codes, artifacts, and unresolved uncertainty. The parent reviews
the diff and reruns compile/tests/quality checks after merge. Never trust a textual
“done” report as verification. *(CoderMageFox/claudecode-codex-subagents · SKILL.md;
Justin-All-In/harness · SKILL.md; korallis/skills-collection · SKILL.md)*

## Hook Coverage Matrix

A hook name or settings entry is not enforcement. Before claiming coverage, record and exercise each boundary:

| Directive | Host event/tool | Registered check | Test payload | Expected exit/effect | Observed result |
|---|---|---|---|---|---|
| read before edit | pre-write/edit | host-specific read-state guard | edit unread file | deny or request read | fill after exercising |
| oracle integrity | pre-commit/CI | `scripts/guard_diff.py` wrapper | remove assertion/add skip | non-zero + finding | fill after exercising |
| evidence on close | stop/CI | `scripts/validate_evidence.py` wrapper | PASS with `not_run` | non-zero + inconsistency | fill after exercising |
| destructive action approval | pre-shell/tool | host policy guard | harmless dry-run fixture representing blocked verb | deny before execution | fill after exercising |

The package ships portable scripts, not a universal hook installer. Host event schemas, exit-code semantics, permissions, and quoting differ; integrate explicitly, keep the host configuration reviewable, and test both allow and deny fixtures. An advisory hook may fail open only when its failure cannot create a false safety claim; a security/completion gate that cannot run must fail closed into `BLOCKED` or `UNVERIFIED`.

## Worktree Isolation

For parallel writable work:

1. Start from a named base revision and require a clean target path; never hide unrelated user changes.
2. Give each worker a separate worktree/branch and disjoint write set. If two workers own one contract, serialize them.
3. Record worktree path, branch/base SHA, owner, intended files, verification command, and handoff SHA/diff.
4. Use a port/resource registry for services so workers do not share ports, databases, caches, or generated outputs accidentally.
5. The parent inspects each diff before integration, resolves conflicts deliberately, then reruns compile/tests/quality gates on the integrated tree.
6. Remove a worktree only after its state is merged or deliberately abandoned and the owner confirms no untracked artifact is needed.

Isolation prevents file collisions; it does not make sub-agent claims trustworthy or eliminate semantic conflicts. *(obra/superpowers · skills/using-git-worktrees/SKILL.md; Wirasm/worktree-manager-skill · SKILL.md; CoderMageFox/claudecode-codex-subagents · SKILL.md)*

## Recovery And Egress

On interruption, write a handoff before losing context. On resume, check whether the
working tree, dependencies, generated artifacts, and external state drifted; then
rerun the relevant gates. External sends, credential movement, and irreversible
actions require explicit consent at the action boundary, not merely at planning.
*(xwtro0tk1t-cloud/harness · SKILL.md; ksimback/looper · SKILL.md;
Myr-Aya/GouvernAI-claude-code-plugin · SKILL.md)*

## Long-Horizon Stop Function

Stop when acceptance is met and evidence is fresh, when a required input is blocked,
when repeated attempts trigger `STOP_AND_ISOLATE`, or when the remaining work is
outside scope. Do not continue for decorative cleanup or keep a loop alive because
the model can generate another patch. *(korallis/skills-collection · SKILL.md;
ksimback/looper · SKILL.md; epicsagas/epic-harness · SKILL.md)*
