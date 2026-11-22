# Exploration And Planning

Load this reference before editing an unfamiliar repository or any request whose
scope is ambiguous. The output is a compact, falsifiable work record, not a prose
essay. The citations are corpus-supplied provenance claims; the archive did not
contain the referenced `03_参考原件/` mirror.

## Reconnaissance Contract

Before changing code, answer with paths and evidence:

1. What user-visible or system behavior is requested?
2. Which files define it, which files import/call it, and which tests exercise it?
3. Which configuration, generated artifacts, public interfaces, migrations, or
   deployment boundaries can change the blast radius?
4. What is explicitly out of scope?
5. Which command will establish the baseline, and what result would falsify the
   current understanding?

Read the complete target file and every directly relevant importer/caller before
editing. Search by symbol and behavior, not only by filename. Use history only to
answer a concrete ownership or compatibility question; do not use it as a ritual.
*(obra/superpowers · skills/writing-plans/SKILL.md; stainless-code/codemap · README.md;
yujiachen-y/codebase-recon-skill · SKILL.md)*

## Scope Record

For a non-trivial change, write this before implementation:

```text
Intent: one behavior sentence.
In scope: exact files or interfaces and the requested delta.
Invariants: behavior that must remain true.
Acceptance: observable checks, including the expected Red failure if applicable.
Risks: callers, data, security, compatibility, performance, and generated output.
Non-goals: adjacent defects deliberately left unchanged.
Blast radius: local | module | public interface | data/deployment.
Baseline: command, exit code, relevant output/artifact.
```

Do not infer that a small diff is low risk. A one-line public-interface change can
have a larger blast radius than a local multi-line fix. *(AlexZio00/sovereign-skills
· skills/ssot-audit/SKILL.md; drafael/coding-harness · skills/blast-radius/SKILL.md)*

## Decomposition

Split work by behavior and verification boundary, not by convenient file count.
Each unit has one owner, one write set, one acceptance check, and one rollback or
containment note. Keep unrelated findings in the report. If two units edit the same
contract, serialize them or make the dependency explicit. *(obra/superpowers ·
skills/subagent-driven-development/SKILL.md; CoderMageFox/claudecode-codex-subagents
· SKILL.md)*

For delegated work, give the worker the relevant paths, constraints, expected
artifact, and exact verification command. Treat its report as a claim until the
parent reruns the relevant checks after merge. *(Justin-All-In/harness ·
skills/readiness-audit/SKILL.md; CoderMageFox/claudecode-codex-subagents · SKILL.md)*

## Plan Review

Reject a plan that:

- edits before identifying the behavior and baseline;
- hides an acceptance check behind “looks good”;
- mixes refactoring with behavior without a reason and comparison check;
- expands scope because the agent noticed a nearby cleanup;
- relies on an unavailable tool without naming the resulting state;
- has no stop condition when evidence contradicts the hypothesis.

The plan is ready when another engineer can predict the first failing check, the
smallest intended edit, and the exact evidence required to close it. *(obra/superpowers
· skills/writing-plans/SKILL.md; svyatov/supermatt · SKILL.md)*

## Small-Change Exception

For a genuinely local, already-understood one-line change, the record may be one
sentence plus one command and one risk note. Still read the target, preserve scope,
and verify the changed behavior. Do not use the exception for public contracts,
security boundaries, migrations, generated files, or unfamiliar code. *(Hexatonic-Lab/
engineering-excellence · SKILL.md; jack-reson8/skill-skill · SKILL.md)*
