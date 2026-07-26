---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-2-11
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Invalid `maxWithdraw()` check in `withdraw()`
vuln_class: []
---

# Invalid `maxWithdraw()` check in `withdraw()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** Vault incorrectly checks `maxWithdraw(receiver)` instead of `maxWithdraw(controller/owner)`.

**Impact:**
- Allows unauthorized withdrawals by exploiting the receiver's limits instead of the owner's.
- DDoS in `withdraw()`

**Proof of Concept:** ❌ Violated: https://prover.certora.com/output/52567/ef88bd2d76b74cafb175f8d026e484b3/?anonymousKey=599db11fbc5df1632ff4006c69a03f836b23fa6c

```solidity
// MUST NOT be higher than the actual maximum that would be accepted
rule eip4626_maxWithdrawNoHigherThanActual(env e, uint256 assets, address receiver, address owner) {

    setup(e);

    storage init = lastStorage;

    mathint limit = maxWithdraw(e, owner) at init;

    withdraw@withrevert(e, assets, receiver, owner) at init;
    bool reverted = lastReverted;

    // Withdrawals above the limit must revert
    assert(assets > limit => reverted, "Withdraw above limit MUST revert");
}
```

✅ Verified after the fix: https://prover.certora.com/output/52567/8e7cfdf612d64a4cb7e5d9d9d939968e/?anonymousKey=a961467ded443bd1cab3718ca882be71f38887e9

**Recommended Mitigation:**
```diff
diff --git a/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol b/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol
index a64f47c..c8824bb 100644
--- a/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol
+++ b/credit-vaults-internal/src/vault/AccountableAsyncRedeemVault.sol
@@ -173,7 +173,7 @@ contract AccountableAsyncRedeemVault is IAccountableAsyncRedeemVault, Accountabl
     function withdraw(uint256 assets, address receiver, address controller) public onlyAuth returns (uint256 shares) {
         _checkController(controller);
         if (assets == 0) revert ZeroAmount();
-        if (assets > maxWithdraw(receiver)) revert ExceedsMaxRedeem();
+        if (assets > maxWithdraw(controller)) revert ExceedsMaxRedeem(); // @certora FIX for eip4626_maxWithdrawNoHigherThanActual (receiver -> controller)

         VaultState storage state = _vaultStates[controller];
         shares = _convertToShares(assets, state.withdrawPrice, Math.Rounding.Floor);
```

**Accountable:** Fixed in commit [`6dc92b0`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/6dc92b0b09e8d2e2fc01b94d41902bbf4f5fc293)

**Cyfrin:** Verified. `controller` now passed to `maxWithdraw`.

\clearpage
