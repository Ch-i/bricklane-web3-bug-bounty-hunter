---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`ExitWithinGracePeriod` event emits inaccurate `amountReceived` for adapter
  vaults'
vuln_class: []
---

# `ExitWithinGracePeriod` event emits inaccurate `amountReceived` for adapter vaults

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** In `SablierBob::exitWithinGracePeriod` (`SablierBob.sol:237-287`), the event always emits the share balance as `amountReceived`:

```solidity
emit ExitWithinGracePeriod(vaultId, msg.sender, amount, amount);
```

For non-adapter vaults this is correct — tokens transfer 1:1 with shares. But for adapter vaults (line 278-280), the actual WETH received depends on the Curve stETH→ETH swap which is subject to slippage:

```solidity
if (address(vault.adapter) != address(0)) {
    vault.adapter.unstakeForUserWithinGracePeriod(vaultId, msg.sender);
} else {
    vault.token.safeTransfer(msg.sender, amount);
}
```

`SablierLidoAdapter::unstakeForUserWithinGracePeriod` does not return the WETH received to the caller, so `SablierBob` has no way to emit the correct value. The adapter emits its own `UnstakeForUserWithinGracePeriod` event with the accurate amount in the same transaction, but the parent `ExitWithinGracePeriod` event's `amountReceived` is misleading.

**Recommended Mitigation:** Have `unstakeForUserWithinGracePeriod` return the WETH received, then use that value in the event:
```solidity
if (address(vault.adapter) != address(0)) {
    uint128 received = vault.adapter.unstakeForUserWithinGracePeriod(vaultId, msg.sender);
    emit ExitWithinGracePeriod(vaultId, msg.sender, received, amount);
} else {
    vault.token.safeTransfer(msg.sender, amount);
    emit ExitWithinGracePeriod(vaultId, msg.sender, amount, amount);
}
```

**Sablier:** Fixed in commit [74fa619](https://github.com/sablier-labs/lockup/commit/74fa619471e00958b6b922f8b6c4d9bb95ccc37a) by removing the early exit grace period functionality.

**Cyfrin:** Verified.
