---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-0-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Incorrect condition
vuln_class: []
---

# Incorrect condition

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

StakingData.sol, line 416: Condition “i < 0” is always false for uint256. Review the functionality

**Recommendation**: 

fix the condition.
