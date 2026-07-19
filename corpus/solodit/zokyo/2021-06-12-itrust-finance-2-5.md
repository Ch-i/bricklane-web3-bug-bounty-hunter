---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-2-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Unused functions
vuln_class: []
---

# Unused functions

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

ITrustVaultFactory.sol: isPaused, _onlyAdmin
Burn.sol: _vaultAddress, _getStartOfDayTimeStamp, validateFactory, _valueCheck
GovernanceDistribution.sol: _getStartOfDayTimeStamp
StakingData.sol: getTotalSupplyForBlock, getHoldingsForIndexAndBlock,
getNumberOfStakingAddresses

**Recommendation**:

Remove unused functions
