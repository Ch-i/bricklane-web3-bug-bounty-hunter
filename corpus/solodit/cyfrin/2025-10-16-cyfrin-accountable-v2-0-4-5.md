---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: ERC20 zero amount transfer rejection
vuln_class: []
---

# ERC20 zero amount transfer rejection

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** The `_checkTransfer` function reverts on zero-amount transfers, violating ERC-20 standard which mandates that transfers of 0 values [MUST be treated](https://eips.ethereum.org/EIPS/eip-20#transfer) as normal transfers.

**Impact:** Violation of `eip20_transferSupportZeroAmount` and `eip20_transferFromSupportZeroAmount`.

**Proof of Concept:** ❌ Violated: https://prover.certora.com/output/52567/9c9c3c73f4d64f9baf1284ced4f4a8f5/?anonymousKey=160f0b0d10e3f688f1981708e4aa3819e7023a80

```solidity
// EIP20-06: Verify transfer() handles zero amount transfers correctly
// EIP-20: "Transfers of 0 values MUST be treated as normal transfers and fire the Transfer event."
rule eip20_transferSupportZeroAmount(env e, address to, uint256 amount) {

    setup(e);

    // Perform transfer
    transfer(e, to, amount);

    // Zero amount transfers must succeed
    satisfy(amount == 0);
}

// EIP20-09: Verify transferFrom() handles zero amount transfers correctly
// EIP-20: "Transfers of 0 values MUST be treated as normal transfers and fire the Transfer event."
rule eip20_transferFromSupportZeroAmount(env e, address from, address to, uint256 amount) {

    setup(e);

    // Perform the transferFrom
    transferFrom(e, from, to, amount);

    // Zero amount transferFrom must succeed
    satisfy(amount == 0);
}
```

✅ Verified after the fix: https://prover.certora.com/output/52567/0babf2c2b4da49ec87cc0ae00036b0e7/?anonymousKey=21b1c4b60901ee2fea0115aa8a1b0e621c04bfaa

**Recommended Mitigation:**
```diff
diff --git a/credit-vaults-internal/src/vault/AccountableVault.sol b/credit-vaults-internal/src/vault/AccountableVault.sol
index 629b6d0..fb3676a 100644
--- a/credit-vaults-internal/src/vault/AccountableVault.sol
+++ b/credit-vaults-internal/src/vault/AccountableVault.sol
@@ -141,7 +141,8 @@ abstract contract AccountableVault is IAccountableVault, ERC20, AccessBase {

     /// @dev Checks transfer restrictions before executing the underlying transfer
     function _checkTransfer(uint256 amount, address from, address to) private {
-        if (amount == 0) revert ZeroAmount();
+        // @certora FIX for eip20_transferSupportZeroAmount and eip20_transferFromSupportZeroAmount
+        // if (amount == 0) revert ZeroAmount();
         if (!transferableShares) revert SharesNotTransferable();
         if (!isVerified(to, msg.data)) revert Unauthorized();
         if (throttledTransfers[from] > block.timestamp) revert TransferCooldown();
```

**Accountable:** Fixed in commit [`e90d3de`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/e90d3de5c133c73f0e783d552bb4e256400a547c)

**Cyfrin:** Verified.
