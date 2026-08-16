---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-1-7
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-13 | Mutability Modifiers
vuln_class: []
---

# UF-13 | Mutability Modifiers

_Section severity (from Solodit section header): Low_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

The `_beetsAlloc`, `_dfyAlloc`, `_treasuryAlloc`, mintFees, and `_earnAmount` variables are never modified, and should therefore be declared `constant`.

**Recommendation**

Declare them as `constant`.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion where appropriate.
