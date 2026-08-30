---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-metamask-totalbalanceenforcer-v2-0
title: Overly restrictive balance consistency check in `TotalBalanceChange` class
  of enforcers can cause potential DoS
vuln_class: []
---

# Overly restrictive balance consistency check in `TotalBalanceChange` class of enforcers can cause potential DoS

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-metamask-TotalBalanceEnforcer-v2.0.md)_

---

**Description:** `TotalBalanceChange` class of enforcers contain a defensive check in `beforeAll` hook that can cause DoS attacks in cross-execution batch scenarios and prevents legitimate balance-modifying enforcers from being used.

The issue stems from overly restrictive validation that assumes balance immutability during the `beforeAll` hook phase.

```solidity
function beforeAllHook(...) public override {
    // ... setup code ...

    uint256 currentBalance_ = IERC20(token_).balanceOf(recipient_);
    if (balanceTracker_.expectedDecrease == 0 && balanceTracker_.expectedIncrease == 0) {
        balanceTracker_.balanceBefore = currentBalance_;
        emit TrackedBalance(msg.sender, recipient_, token_, currentBalance_);
    } else {
        // @audit Overly restrictive check can prevent legitimate enforcers
        require(balanceTracker_.balanceBefore == currentBalance_, "ERC20TotalBalanceChangeEnforcer:balance-changed");
    }
    // ...
}
```
The check above assumes that there would not be any enforcers that can change state in the `beforeAll` hook. Imagine a `prepaymentEnforcer` implemented in future that requires upfront token transfer before execution (eg. fees or collateral moved to an escrow account) - current balance validation will make the `TotalBalanceChange` enforcers incompatible with such enforcers.

Consider following batch execution scenario:

```solidity
// Execution 1: Bob uses TotalBalanceChangeEnforcer for Alice
// Execution 2: Dave uses PrepaymentEnforcer + TotalBalanceChangeEnforcer for Alice

// Attack flow:
// 1. Exec1 TotalBalanceChangeEnforcer.beforeAllHook: Sets balanceBefore = Alice's current balance
// 2. Exec2 PrepaymentEnforcer.beforeAllHook: Collects 1 ETH from Alice → Alice balance changes
// 3. Exec2 TotalBalanceChangeEnforcer.beforeAllHook: require(old_balance == new_balance) → REVERT
// 4. Entire batch transaction fails
```

**Impact:** Overly restrictive validation can DoS entire batch transactions when specific enforcer combinations are at play.


**Recommended Mitigation:** Consider replacing the restrictive balance consistency check with simple overwriting. Overwriting would mean that the last `TotalBalanceChangeEnforcer` becomes the baseline for all `afterAllHook` operations.

Current balance check is not adding any value from a "security" standpoint but adds DoS and enforcer incompatibility risks.


```solidity
function beforeAllHook(...) public override {
    // ... setup code ...

    uint256 currentBalance_ = IERC20(token_).balanceOf(recipient_);

    if (balanceTracker_.expectedDecrease == 0 && balanceTracker_.expectedIncrease == 0) {
        balanceTracker_.balanceBefore = currentBalance_;
        emit TrackedBalance(msg.sender, recipient_, token_, currentBalance_);
    } else {
        // @audit Update baseline to current balance instead of requiring equality
        balanceTracker_.balanceBefore = currentBalance_;
    }
    // ...
}
```


**Metamask:** Fixed in [PR 144](https://github.com/MetaMask/delegation-framework/pull/144/commits/1e49f851b4bc09987969ed9426f59d3d40af3828).

**Cyfrin:** Verified.

\clearpage
