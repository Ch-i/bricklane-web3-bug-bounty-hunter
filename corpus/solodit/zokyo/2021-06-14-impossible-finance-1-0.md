---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Different Solidity versions.
vuln_class: []
---

# Different Solidity versions.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

Different pragma directives are used. Throughout the project (including interfaces). Version
used: '=0.5.16', '>=0.5.0'
Issue is classified as Medium, because it is included to the list of standard smart contracts’
vulnerabilities.

**Recommendation**:

Use the same pragma directives for the entire project.
