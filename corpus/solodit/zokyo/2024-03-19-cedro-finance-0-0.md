---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-0-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Method `depositRequest(...)` allows the last deposit to be more than the set
  deposit cap
vuln_class: []
---

# Method `depositRequest(...)` allows the last deposit to be more than the set deposit cap

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In Contract Branch.sol, the method `depositRequest()` checks if the `depositCap` has been reached before processing any deposit.

```solidity
       if (depositCapReached[id]) revert DepositCapReached(TAG, id);
```
However, the deposit cap reached is set as follows:
```solidity
if (liquidity > capAmount[id]) {
           depositCapReached[id] = true;
       }
```
Here the liquidity is calculated after tokens have been deposited and if liquidity is more than the cap amount, it does not revert.

For eg.

- ADMIN sets capAmount for MATIC as 1 million

- User A deposits 0.99 million MATIC and depositCapReached is still false as liquidity < capAmount.

- User B deposits 5 million MATIC and depositCapReached is set as true as liquidity > capAmount.

- Now total deposited MATIC is 5.99 million where whereas the set cap was 1 million only.

- This way a user can deposit much more than the set cap.

**Recommendation**: 

Update the method `depositRequest()` to revert if the current deposit is more than the `setCap` for that particular pool id.
