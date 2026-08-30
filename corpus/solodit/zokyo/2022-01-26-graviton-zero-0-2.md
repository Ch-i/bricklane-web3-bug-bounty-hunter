---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-01-26-graviton-zero-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-01-26T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-01-26-Graviton%20Zero.md
tags:
- firm:zokyo
- report:2022-01-26-graviton-zero
title: Risk of underflow
vuln_class: []
---

# Risk of underflow

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-01-26-Graviton Zero.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-01-26-Graviton%20Zero.md)_

---

**Description**

StakingB_1.sol Line 579
Each user can use the unstake function even if they have nothing to unstake, so everyone can
decrease the “amountOfUsers” variable that can cause an underflow and won’t allow other
users to unstake.

**Recommendation**:

Check if “userInfo[msg.sender]” has not been already deleted before decreasing an
“amountOfUsers”.
