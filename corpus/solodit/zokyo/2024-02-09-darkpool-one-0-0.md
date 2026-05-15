---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-02-09-darkpool-one-0-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-02-09T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-09-Darkpool%20One.md
tags:
- firm:zokyo
- report:2024-02-09-darkpool-one
title: Certain ERC20 tokens do not return bool from approve which breaks the core
  logic
vuln_class: []
---

# Certain ERC20 tokens do not return bool from approve which breaks the core logic

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-02-09-Darkpool One.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-02-09-Darkpool%20One.md)_

---

**Severity**: High

**Status**:  Resolved

**Description**

The BrightPoolLenger and UniswapExchange contracts attempt to approve the ask or bid token for other contracts and require the approve function to return true. However, some ERC20 implementations (e.g., mainnet USDT) do not return a value. This will cause a revert when the implementation tries to decode the boolean return value of the call to approve.
```solidity
if (!order.bid.token.approve(address(exchangeable), order.bid.amount)) revert InsufficientFunds();
```
However, some ERC20 implementations (e.g., mainnet USDT) do not return a value. This will cause a revert when the implementation tries to decode the boolean return value of the call to approve.

**Recommendation**: 

Consider using SafeApprove instead of approve.
