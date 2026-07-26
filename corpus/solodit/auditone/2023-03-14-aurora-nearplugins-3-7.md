---
affected_contracts: []
derives_from: []
id: solodit-auditone-2023-03-14-aurora-nearplugins-3-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-03-14T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md
tags:
- firm:auditone
- report:2023-03-14-aurora-nearplugins
title: Missing documentation for the case of using Upgradable to patch a vulnerability
vuln_class: []
---

# Missing documentation for the case of using Upgradable to patch a vulnerability

_Section severity (from Solodit section header): Informational_  
_Audit firm: AuditOne_  
_Source report: [2023-03-14-Aurora_NEARplugins.md](https://github.com/solodit/solodit_content/blob/main/reports/AuditOne/2023-03-14-Aurora_NEARplugins.md)_

---

**Description:** 

Before deployment all code is kept in up\_stage\_code. If deployment is made for security issue then up\_stage\_code will contain fix for vulnerable code which could be seen by users to exploit current codebase.

- User reports a critical vulnerability in contract code
- Owner quickly make patch and calls up\_stage\_code to write the updated code
- Before owner could deploy, attacker checks this upstage code, figures out the vulnerability and exploits it

**Recommendations:** 

For critical upgrades, encrypted code could be upstaged which could be decrypted at deployment time using a provided key.
