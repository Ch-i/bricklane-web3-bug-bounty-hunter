---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Share variables lack validation.
vuln_class: []
---

# Share variables lack validation.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Disqualifier.sol: setHunterShare(). 
Eligibility DataProvider.sol: setRequired EthRatio(). 
Middle Fee Distribution.sol: setLpLocking Reward Ratio(), setOperation Expenses(). 
Leverager.sol: setFeePercent(). 
Leverager.sol: loop(), parameter 'borrowRatio (Should be validated not to exceed 10 ** 
BORROW_RATIO_DECIMALS'). 
Radiant OFT.sol: setFeeInfo(). 
StargateBorrow.sol: setXChain Borrow Fee Percent(). 
Some of the variables act as shares or use shares during calculations, however such variables lack validation, that they don't exceed 100%. For example, in Disqualifier.sol when setting HUNTER_SHARE, the contract should validate that the new value will not exceed 10000 (As division is performed with 10000 as a denominator in line 277). Issue is marked as low-risk since only owner can set these variables, though in case of invalid value it will affect the correctness of calculations in the protocol. 

**Recommendation**: 

Validate that share variable doesn't exceed 100%.
