---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Unlimited allowance.
vuln_class: []
---

# Unlimited allowance.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

LockZap.sol: constructor(), lines 53-54; setLpMfd(), line 66. 
Making an unlimited allowance of tokens might be potentially dangerous and lead to funds loss in case of exploitation. Though approval is performed on protocol contracts (Uniswap PoolHelper.sol or Balancer PoolHelper.sol and MultiFee Distribution.sol) these contracts are upgradeable. This is why approving tokens before each transfer on the amount necessary for a particular transfer is recommended. 

**Recommendation**: 
Approve tokens, necessary for transfer before each transfer operation instead of granting an unlimited allowance. 

**Post-audit**. 

Unlimited allowance was removed.
