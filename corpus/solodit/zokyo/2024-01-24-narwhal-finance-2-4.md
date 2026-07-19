---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Method `distributeRewardUSDT` can increment `currentBalanceUSDT` without sending
  USDT
vuln_class: []
---

# Method `distributeRewardUSDT` can increment `currentBalanceUSDT` without sending USDT

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

In Contract TradingVault, method distributeRewardUSDT(...) has a boolean value to check if USDT needs to be transferred from msg.sender or not. 
In case _send is false and USDT is not already transferred, currentBalanceUSDT will be increased by _amount which can lead to wrong calculation of shares and assets.

**Recommendation**: 

Add a check to ensure that `currentBalanceUSDT` is equal to amount of USDT tokens in the contract.
