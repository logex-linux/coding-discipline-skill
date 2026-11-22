# Security Policy

## Supported Versions

Only the latest revision on the default branch is supported.

## Reporting A Vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub's private security advisory flow for this repository and include:

- affected file and revision;
- a minimal reproduction or malicious input;
- actual versus expected behavior;
- impact and any known workaround.

Do not include live credentials, private repository contents, or unrelated user data. A report will be triaged before any public disclosure.

## Scope

Relevant issues include command construction, path traversal, secret exposure, unsafe diff/receipt parsing, bypasses in deterministic guards, and misleading security claims in the skill carrier. The scripts are intentionally non-executing where possible; `validate_evidence.py` never replays receipt commands.
