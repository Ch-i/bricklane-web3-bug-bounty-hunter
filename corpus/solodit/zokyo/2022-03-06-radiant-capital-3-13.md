---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-13
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Verification of oracles' implementation.
vuln_class: []
---

# Verification of oracles' implementation.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

UniV3TwapOracle.sol: getPrecisePrice(), lines 73, 79. 
In case, value of 'decimals1' or 'decimals' is greater than 18, an overflow will occur. 
Though such a case where a token has more than 18 decimals is rare, such functionality should still be verified. 
1. UniV2TwapOracle.sol: consult(), line 118. 
Price is requested for a value '1 ether', thus in case token has any other number of decimals but 18, consult() will return an invalid price. 
2. Base Oracle.sol 
It should be noted that the owner of the contract can set any fallbackOracle at any time, thus affecting the price returned by oracle. Though it is not a security issue, it still should be noted in the final report. 

**Recommendation**: 

Correct the natspec or the name of functions locked UsdValue() and required UsdValue() so that it is clear in which units the value is returned. Verify the correctness of comparison or bring values to the same units. 

**Post-audit**: 
In function required UsdValue(), variable 'totalCollateralETH', taken from LendingPool, was renamed into 'totalCollateralUSD'. However no changes were applied in LendingPool, thus LendingPool still returns value in ETH. 
**Post-audit**: 
According to the Radiant Capital team, when AaveOracle is deployed, its base currency will be set as USD. Thus functions such as getUserAccountData() in LendingPool will return values in USD, not ETH.
