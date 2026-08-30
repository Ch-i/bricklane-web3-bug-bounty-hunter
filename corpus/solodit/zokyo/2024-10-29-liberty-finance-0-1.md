---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-29-liberty-finance-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md
tags:
- firm:zokyo
- report:2024-10-29-liberty-finance
title: Method ownerDepositForDistribution should check if enough tokens present in
  the rewards contract
vuln_class: []
---

# Method ownerDepositForDistribution should check if enough tokens present in the rewards contract

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-10-29-Liberty Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-29-Liberty%20Finance.md)_

---

Severity: Low

Status: Resolved

**Description**

In Contract Rewards.sol, the method ownerDepsoitForDistribution(..) sets a distribution amount but does not check if enough tokens are present in the contract to distribute such an amount. In the case there are not enough tokens, distributeRewards() will fail unless tokens are transferred.

Also, this method does not need nonReentrant modifier as it can be called only by owner and there are no transfer of tokens here.

**Recommendation**: 

Add a check to ensure enough tokens are present in the contract when the distribution amount is being set.
