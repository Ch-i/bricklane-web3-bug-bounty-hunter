---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Owner is able to withdraw staking token.
vuln_class: []
---

# Owner is able to withdraw staking token.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

MultiFee Distribution.sol: recoverERC20(). 
The owner can directly access users' funds and withdraw their tokens anytime since the owner can't recover only reward tokens. As a result, in the case of the private key exploit (of an owner account), users' funds can be withdrawn directly from the contract. That's why it is recommended to validate that the provided 'tokenAddress is not a staking token, in order to exclude a centralization risk. 

**Recommendation**: 

Validate that 'tokenAddress' is not a staking token in the function. 

**Post-audit**. 

Function recoverERC20() was removed.
