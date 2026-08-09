---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-6 | Using .transfer
vuln_class: []
---

# UF-6 | Using .transfer

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

`transfer()` comes with a fixed amount of gas.

**Recommendation**

Utilize `call()` with a success check.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion.
