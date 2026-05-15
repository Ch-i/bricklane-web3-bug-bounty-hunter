---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-12
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: ETH value is compared to USD value.
vuln_class: []
---

# ETH value is compared to USD value.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Eligibility DataProvider.sol: isEligible ForRewards(), line 205. 
The function validates that the user's locked value >= user's required value (with functions lockedUsdValue() and required UsdValue() respectively). 
The name of the function locked UsdValue() implies, that it will return value in USD, the natspec section (line 152) states that value is returned in ETH. In fact, the value is returned in USD. Thus the variable 'lockedValue is in USD units. 
The name of the function required UsdValue() implies, that it will return value in USD, the natspec section (lines 167-168) states that value is returned in ETH. In fact, the value is returned in ETH. Thus the variable 'requiredValue' is in ETH units. 
Thus when 'lockedValue' and 'requiredValue` are compared to each other, ETH value is compared to USD value, which is not a correct comparison. That leads to incorrect determining if user is eligible for rewards. Issue is marked as info, as it should be verified by the Radiant team if such functionality is valid. 

**Recommendation**: 

Correct the natspec or names of functions locked UsdValue() and required UsdValue(). It should be clear in which units the value is returned. Verify the correctness of comparison or bring values to the same units. 

**Post-audit**: 

In function required UsdValue(), variable 'totalCollateralETH', taken from LendingPool, was renamed into 'totalCollateralUSD. However no changes were applied in LendingPool, thus LendingPool still returns value in ETH. 

**Post-audit**: 

According to the Radiant Capital team, when AaveOracle is deployed, its base currency will be set as USD. Thus functions such as getUserAccountData() in Lending Pool will return values in USD, not ETH.
