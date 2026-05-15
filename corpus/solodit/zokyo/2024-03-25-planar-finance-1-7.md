---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-25-planar-finance-1-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md
tags:
- firm:zokyo
- report:2024-03-25-planar-finance
title: Addressing the Approve Race Condition with `safeIncreaseAllowance` and `safeDecreaseAllowance`
  in Smart Contracts
vuln_class: []
---

# Addressing the Approve Race Condition with `safeIncreaseAllowance` and `safeDecreaseAllowance` in Smart Contracts

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-03-25-Planar Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-25-Planar%20Finance.md)_

---

**Severity**: Low

**Status**:  Unresolved


**Location**: XplaneToken, line 252 

**Description**:

The provided `approveUsage` function is designed to set an approval amount for a specific usage by an external contract or entity. However, it directly sets the approval amount to a new value without considering the potential risks associated with approval race conditions. This vulnerability is inherent in the ERC-20 token standard's approve function and can similarly affect custom approval mechanisms like the one described.

**The Race Condition Explained**:

The race condition occurs when a user attempts to adjust an already granted allowance. Suppose a user wants to change an allowance from 100 to 200 tokens. They send a transaction to update this allowance, but just before this transaction is confirmed, a malicious actor uses the original allowance of 100 tokens. If the update transaction then goes through, the malicious actor could potentially spend up to 300 tokens (100 before the allowance change and 200 after), exploiting the gap between these transactions.

This issue arises because the approve function (or similar custom functions, as in the `approveUsage` example) replaces the existing allowance with a new value, without locking the allowance during the update process. This creates a window where the allowances can be misused.

**Solution with safeIncreaseAllowance and safeDecreaseAllowance**:

A safer approach involves using two functions: `safeIncreaseAllowance` and `safeDecreaseAllowance`,
`safeIncreaseAllowance` safely increases the allowance by a certain amount, ensuring that the increase is additive to the current allowance, reducing the risk of the race condition.
`safeDecreaseAllowance` safely decreases the allowance by a specified amount, ensuring that the decrease cannot be exploited to spend more than intended.
