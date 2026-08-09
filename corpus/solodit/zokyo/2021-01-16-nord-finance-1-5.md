---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-01-16-nord-finance-1-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2021-01-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md
tags:
- firm:zokyo
- report:2021-01-16-nord-finance
title: DRY, slot manipulation methods (setBoolean, getBoolean, setAddress, getAddress,
  setUint256, getUint256) are duplicated across two contracts.
vuln_class: []
---

# DRY, slot manipulation methods (setBoolean, getBoolean, setAddress, getAddress, setUint256, getUint256) are duplicated across two contracts.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-01-16-Nord Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-01-16-Nord%20Finance.md)_

---

**Recommendation**:

Move that methods to separate contract or library.
