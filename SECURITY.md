# Security Policy

## Purpose Statement

web3Sentinel is a **defensive** smart contract security audit harness. It aggregates publicly available vulnerability data from sources such as Solodit, arXiv, rekt.news, Sherlock, Code4rena, Cantina, and Immunefi to help security researchers, auditors, and developers identify and remediate smart contract weaknesses.

This tool is intended exclusively for defensive security research, education, and audit preparation. It must not be used to exploit live contracts, exfiltrate funds, or conduct any unauthorized offensive activity.

## Responsible Disclosure

If you discover a security vulnerability in Bricklane, please report it privately. **Do not open a public issue.**

- **Email:** [security@bricklane.dev](mailto:security@bricklane.dev)
- **Subject line format:** `[SECURITY] Brief description of the issue`
- **Include in your report:**
  - A clear description of the vulnerability and its potential impact
  - Steps to reproduce
  - Affected component(s) (e.g., crawler, API, UI, on-chain verification module)
  - Any suggested remediation, if applicable

Encrypt sensitive reports with our PGP key if one is published in this repository.

## Scope

The following are considered valid security vulnerabilities in this project:

| Category | Examples |
|---|---|
| **Authentication & Authorization** | API auth bypass, privilege escalation, broken access controls |
| **Data Exposure** | Leakage of API keys, credentials, session tokens, or user-specific data |
| **Injection & Input Handling** | SQL injection, command injection, XSS, or SSRF in the UI or API |
| **Dependency Vulnerabilities** | Known CVEs in third-party packages used by Bricklane |
| **On-Chain Verification** | Flaws in the verification logic that could produce false positives/negatives or leak private keys |
| **Crawler Integrity** | Vulnerabilities allowing poisoned or tampered data to bypass ingestion validation |
| **Infrastructure** | Misconfigurations exposing internal services, debug endpoints, or secrets |

## Out of Scope

The following are **not** considered vulnerabilities in Bricklane:

- **Public vulnerability corpus data** — the exploit descriptions, pattern summaries, and audit findings ingested from public sources are intentionally accessible and not confidential.
- **Public exploit transaction hashes** — on-chain transaction hashes referenced in the dataset are part of the permanent public blockchain record.
- **Pattern descriptions and detection rules** — classification heuristics and vulnerability pattern metadata are project knowledge, not secrets.
- **Bugs in upstream data sources** — issues in Solodit, arXiv, rekt.news, or other ingested platforms should be reported to those projects directly.
- **Theoretical attacks requiring physical access** to the host machine.
- **Social engineering** of project maintainers or contributors.

## Response Timeline

We are committed to addressing security reports promptly:

| Milestone | Target |
|---|---|
| **Acknowledgement** | Within **48 hours** of receipt |
| **Initial assessment** | Within **72 hours** — severity classification and affected components identified |
| **Critical fix** | Within **7 days** of confirmation |
| **High-severity fix** | Within **14 days** of confirmation |
| **Medium/Low fix** | Within **30 days**, or in the next scheduled release |
| **Disclosure coordination** | We will coordinate public disclosure timing with the reporter |

If a fix requires more time, we will communicate the revised timeline and keep the reporter informed.

## Legal

We consider good-faith security research to be authorized and welcome it. We will **not** initiate legal action against researchers who:

- Act in good faith and follow this disclosure policy
- Avoid accessing, modifying, or deleting data belonging to other users
- Do not degrade the availability of Bricklane services
- Report vulnerabilities privately before any public disclosure
- Allow reasonable time for remediation before disclosure

This safe harbor applies to activity conducted under this policy. It does not extend to unlawful activity unrelated to security research on this project.

## Attribution

We believe in recognizing the security community's contributions:

- Reporters will be **credited by name** (or chosen handle) in the project `CHANGELOG` upon fix release, unless they request anonymity.
- To opt out of public attribution, state your preference in your initial report.
- We are happy to provide a reference letter or verification of your contribution upon request.

---

*This policy is effective as of June 2026 and applies to all components of the Bricklane project, including crawlers, API, UI, and on-chain verification modules.*
