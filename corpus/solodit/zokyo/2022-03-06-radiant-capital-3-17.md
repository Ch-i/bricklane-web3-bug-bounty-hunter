---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-17
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Variable is initialized in storage in upgradable smart contract.
vuln_class: []
---

# Variable is initialized in storage in upgradable smart contract.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

UniV3TwapOracle.sol: 'lookbackSecs`. 
Storage variables can't be initialized outside of functions in upgradable smart contracts. 
Thus variable 'lookbackSecs will be initially equal to 0. Issue is marked as info, since smart contract has additional setter for this variable. 

**Recommendation**: 

Initialize variable in initializer() function.
