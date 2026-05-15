---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-06-08-yield-farming-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-06-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md
tags:
- firm:zokyo
- report:2022-06-08-yield-farming
title: Contracts UnifarmCohort, UnifarmNftManagerUpgradeable, etc... are making use
  of SafeMath for mathematical operations, but since the solidity 0.8.0, the use of
  SafeMath is not necessary anymore because the revert happens automatically in cas
vuln_class: []
---

# Contracts UnifarmCohort, UnifarmNftManagerUpgradeable, etc... are making use of SafeMath for mathematical operations, but since the solidity 0.8.0, the use of SafeMath is not necessary anymore because the revert happens automatically in case of overflow or underflow, so SafeMath is not adding any benefits and it’s just making taking more gas with no addeds benefits.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-06-08-Yield Farming.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md)_

---

**Recommendation**:
Remove the use of SafeMath library and the use of it’s methods and replace them with normal
signs calculations. (Done we removed the SafeMath Now)
