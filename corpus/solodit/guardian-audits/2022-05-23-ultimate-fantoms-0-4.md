---
affected_contracts: []
derives_from: []
id: solodit-guardian-audits-2022-05-23-ultimate-fantoms-0-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-05-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md
tags:
- firm:guardian-audits
- report:2022-05-23-ultimate-fantoms
title: UF-5 | Price Inconsistency
vuln_class: []
---

# UF-5 | Price Inconsistency

_Section severity (from Solodit section header): Medium_  
_Audit firm: Guardian Audits_  
_Source report: [2022-05-23-Ultimate Fantoms.md](https://github.com/solodit/solodit_content/blob/main/reports/Guardian%20Audits/2022-05-23-Ultimate%20Fantoms.md)_

---

**Description**

In the `getPrice` function the stepwise price jumps do not account for the following `tokenIds`: 101,
301, 601, 1001, 1501, and 2301.
This is because each if statement utilizes > instead of >= when referring to these tokenIds.Therefore
a mint for one of these `tokenIds` will mistakenly go to the else branch and charge 6 `FTM`.

**Recommendation**

Use `>=` or decrement the lower boundaries by one.

**Resolution**

Ultimate Fantoms: Resolved, applied suggestion.
