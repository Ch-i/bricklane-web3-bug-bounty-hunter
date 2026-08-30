---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: '`SablierLidoAdapter::unstakeFullAmount` should return `totalWstETH`'
vuln_class: []
---

# `SablierLidoAdapter::unstakeFullAmount` should return `totalWstETH`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** `SablierBob::_unstakeFullAmountViaAdapter` always calls `SablierLidoAdapter::getTotalYieldBearingTokenBalance` then `SablierLidoAdapter::unstakeFullAmount`:

* `SablierLidoAdapter::getTotalYieldBearingTokenBalance` just reads and returns `_vaultTotalWstETH[vaultId]`
* the first thing `SablierLidoAdapter::unstakeFullAmount` does is perform an identical storage read of `_vaultTotalWstETH[vaultId]`

This is inefficient; there are two identical storage reads and one redundant external call. Simply have `SablierLidoAdapter::unstakeFullAmount` return `_vaultTotalWstETH[vaultId]`:
```diff
    function unstakeFullAmount(uint256 vaultId)
        external
        override
        onlySablierBob
-       returns (uint128 amountReceivedFromUnstaking)
+       returns (uint128 totalWstETH, uint128 amountReceivedFromUnstaking)
    {
        // Get total amount of wstETH in the vault.
-       uint128 totalWstETH = _vaultTotalWstETH[vaultId];
+       totalWstETH = _vaultTotalWstETH[vaultId];
```

Then change `SablierBob::_unstakeFullAmountViaAdapter` to use it:
```diff
    function _unstakeFullAmountViaAdapter(uint256 vaultId) private returns (uint128 amountReceivedFromAdapter) {
        Bob.Vault storage vault = _vaults[vaultId];

-       // Get the total amount staked via the adapter.
-       uint128 amountStakedViaAdapter = vault.adapter.getTotalYieldBearingTokenBalance(vaultId);

        // Interaction: unstake all tokens via the adapter.
-       amountReceivedFromAdapter = vault.adapter.unstakeFullAmount(vaultId);
+       uint128 amountStakedViaAdapter;
+       (amountStakedViaAdapter, amountReceivedFromAdapter) = vault.adapter.unstakeFullAmount(vaultId);

        // Log the event.
        emit UnstakeFromAdapter(vaultId, vault.adapter, amountStakedViaAdapter, amountReceivedFromAdapter);
    }
```

**Sablier:** Fixed in commit [d812e23](https://github.com/sablier-labs/lockup/commit/d812e2325975748019f5108f5fa87070e92fa753).

**Cyfrin:** Verified.
