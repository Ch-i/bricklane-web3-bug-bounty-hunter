---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Use storage pointer
vuln_class: []
---

# Use storage pointer

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

StakingData.sol, line 308, _getAllAcountUnstakesForAddress()
StakingData.sol, line 287, _getAccountStakesForAddress()
StakingData.sol, line 225, _getRoundRewardsForAddress()
RoundData.sol, line 15, endRound()
Burn.sol, line 64, getCurrentBurnData()
Burn.sol, line 77, startBurn()
Burn.sol, line 140, endBurn()
Consider usage of storage pointer to mapping member in order to get gas savings since the
function has several calls to this data.

**Recommendation**:

Use storage pointer.
