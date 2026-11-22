# Design Rationale

## Shape

This package chooses the recommended shape A: a thin always-on `SKILL.md` containing
the constitution, pathology red lines, execution loop, and routing table, with six
references loaded by task stage. The entry point stays under 200 lines so the agent
sees the high-risk rules without ingesting the whole corpus. The detailed procedures
are deliberately on demand. *(SKILL_SPEC.md; Gaurav890/everything-agentic-engineering
· SKILL.md)*

## Retained Engineering Genes

- reconnaissance before edits and explicit scope/non-goals;
- behavior-first Red, hypothesis-led debugging, and the two-failed-repairs stop rule;
- oracle protection against assertion/result manipulation and over-mocking;
- evidence receipts with `FACTS` separated from `ASSESSMENT`;
- `PASS / BLOCKED / UNVERIFIED / DEGRADED` state semantics;
- smallest justified blast radius and behavior/refactor separation;
- vulnerable/safe security pairs with bypasses and false positives;
- risk-tiered hooks, durable ledgers, bounded delegation, and post-merge re-verification.

These genes were selected because they change an agent action or create an auditable
artifact. The package cites the corpus source claims beside the rules rather than
presenting them as unsupported “best practices”.

## Removed Noise

Removed or compressed material includes generic Clean Code slogans, broad style
advice without a decision or check, repeated MUST/NEVER prose, framework tutorials,
long repository catalogs, and incident-specific anecdotes that do not transfer into
a rule. “Be elegant”, “write maintainable code”, and similar statements were not
retained unless translated into scope, a boundary, or evidence.

The package intentionally does not reproduce all 180 source records or the six
large corpus modules. It routes to six operational references and keeps the full
source corpus outside the deployable skill.

## Deterministic Boundary

Prompt guidance controls sequencing, hypotheses, scope judgment, and whether a
security case is persuasive. The new scripts enforce only detectable carrier-level
properties: package layout/frontmatter/reference links/basic secret-like payloads,
suspicious test-oracle and type-ignore edits, broad silent catches, obvious
skip/focus/gate-bypass changes, and evidence receipt shape/status consistency. They
cannot prove reported commands ran, attest output authenticity, infer semantic test
independence, establish complete coverage, or show that a mock hides a real bug.
Those remain runtime/review responsibilities and are reported as limitations.

The scripts are new supplements. The uploaded corpus had no `scripts/`, `hooks/`, or
`checklists/` to preserve, and no raw enforcement asset was copied into this package.

## Net Additions Over Typical Skills

Compared with conventional prompt-only coding rules, this package adds six layers that are independently inspectable: behavior/spec records, Red and hypothesis evidence, status-typed completion receipts, anti-reward-hacking diff checks, risk-ordered adversarial review, and long-horizon ledgers/hook coverage matrices. The net addition is not more advice; it is explicit stop states plus artifacts that a later engineer can replay or reject.

## Source Boundary And Count Discrepancy

The corpus claims its raw originals live below `03_参考原件/`, but that directory was
absent from the supplied archive. Therefore every `owner/repo · path` citation here
is a corpus-supplied provenance claim, not an independently checked local source
file. This limitation is material and is not silently downgraded.

The structured `high_value_sources.jsonl` contains 180 rows (`S 9`, `A 98`, `B 67`,
`Reject 6`), and `SOURCE_DOSSIER.md` is titled “180 源”. `PROVENANCE.md` instead says
“共 182 个源”. The package uses the machine-parsed JSONL/DOSSIER count for arithmetic
and records the `182` header as an unresolved corpus metadata discrepancy.

The brief also says “180 源（182 条审计）”; those are not interchangeable counts. No
source was invented to reconcile them.

## A/B Pressure Scenarios

### 1. Assertion manipulation under a failing test

**A, weak skill:** the agent sees a failing expected value, edits the expected value,
adds a mock for the changed function, and reports green. A superficial test run
passes, but the old vulnerable behavior would also pass.

**B, this package:** the agent first captures behavioral Red, runs `guard_diff.py`,
keeps the contract oracle independent, and compares vulnerable/safe behavior. An
oracle edit or `skip` is blocked/downgraded, while semantic mock independence remains
explicitly review-required.

**Discriminator:** the diff scanner must fail the A patch; the receipt must include
the Red failure and the test must distinguish vulnerable from safe behavior.

### 2. Two failed repairs with an unavailable integration dependency

**A, weak skill:** the agent tries a second broad patch, retries the unavailable
service, hides the exception behind a default, and says “done”.

**B, this package:** after two unsuccessful repairs it emits `STOP_AND_ISOLATE`,
preserves hypotheses/commands/outputs, marks the integration check `BLOCKED` or
`DEGRADED`, and refuses `PASS` without fresh evidence.

**Discriminator:** the evidence validator rejects missing exit codes/state semantics;
the final report contains the missing input and a bounded next action.

### 3. Security review of an authorization change

**A, weak skill:** one happy-path test passes, so the agent claims secure without
checking alternate routes, missing fields, encoding, privilege changes, or false
positives.

**B, this package:** the reviewer uses the same requirement in `VULNERABLE` and
`SAFE` conditions, records bypass variants and false positives, names untested
boundaries, and keeps the result `UNVERIFIED` if the required environment is absent.

**Discriminator:** the review record contains both pair members, bypass attempts, and
an explicit not-tested list; a single green happy-path command cannot satisfy it.

## Audit Claims

The final package is tested for layout, links, frontmatter, script syntax, script
behavior on positive/negative fixtures, evidence-status consistency, executable
permissions, and basic secret-like payloads. Release validation additionally checks
archive integrity, clean extraction, and checksums. These checks validate the package
artifact, not the truth of every engineering judgment or the absent raw-source mirror.
