---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Missing result assignment
vuln_class: []
---

# Missing result assignment

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

Burn.sol, line 130. “_burnData[vaultAddress].totalBurned.add(toBurn);”
Total burned value is not updated - addition result is not placed to storage.

**Recommendation**:
fix the condition.
