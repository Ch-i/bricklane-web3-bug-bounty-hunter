---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-05-09-aurorafastbridge-3-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-05-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md
tags:
- firm:auditone
- report:2023-05-09-aurorafastbridge
title: 'Out-of-date Rust Crate Detected with Cargo Audit Severity: Quality Assurance'
vuln_class: []
---

# Out-of-date Rust Crate Detected with Cargo Audit Severity: Quality Assurance

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-05-09-Aurorafastbridge.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-05-09-Aurorafastbridge.md)_

---

**Description:** 

A recent cargo audit has detected an out-of-date Rust crate within the project. Cargo audit is a tool that analyzes the Rust project's dependency tree and reports any known security vulnerabilities or outdated dependencies. Using outdated crates can introduce potential risks and negatively affect the performance, stability, and security of the application.

**Recommendations:** 

To address this issue, it is recommended to update the out-of-date crate to its latest version, ensuring that any security vulnerabilities, bug fixes, or new features are incorporated into the project.
