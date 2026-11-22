## Summary

- behavior and scope changed:
- deterministic backstops changed:
- explicit non-goals:

## Evidence

- Red command / expected failure:
- focused verification command / exit code:
- broader checks / exit codes:
- guard diff result:

## Risk Review

- blast radius:
- compatibility/data/security concerns:
- not-run checks and reason:
- residual risks:

## Oracle Integrity

- [ ] No assertion, matcher, threshold, expected value, skip/focus marker, type rule, or CI gate was weakened without an independently documented requirement.
- [ ] The regression test fails against the known-bad behavior and passes against the candidate fix.
- [ ] Refactoring and behavior changes are distinguishable.
