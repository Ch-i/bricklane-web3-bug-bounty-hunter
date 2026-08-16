---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Storage variables are never used.
vuln_class: []
---

# Storage variables are never used.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

AutoCompounder.sol: 'rdntToken', 'IpTokenAddress', 'baseToRdnt'. 
Eligibility DataProvider.sol: 'baseToken PriceInUsd ProxyAggregator'. 
Disqualifiers.sol: treasury`. 
MiddleFee Distribution.sol: 'minters', 'mintersAreSet'. 
Variables are never used in the contract's logic, and some variables are even never set. 
*baseToRdnt is initialized with zero addresses. The unused variable can mean that the contract is unfinished, so it is recommended not to have such variables. 

**Recommendation**: 

Remove unused variables OR finish contract's logic where variables will be used OR verify that these variables are necessary to other smart-contracts or the Dapp.
