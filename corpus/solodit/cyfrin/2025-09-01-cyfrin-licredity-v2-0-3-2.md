---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-3-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Reentrancy via `stagedFungible` not cleared before external call
vuln_class: []
---

# Reentrancy via `stagedFungible` not cleared before external call

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** In [`Licredity::exchangeFungible`](https://github.com/Licredity/licredity-v1-core/blob/e8ae10a7d9f27529e39ca277bf56cef01a807817/src/Licredity.sol#L217-L222), the transient `stagedFungible` flag is cleared only after the external call `baseFungible.transfer(recipient, amountOut)`. If the base token supports transfer callbacks (e.g., ERC777-like hooks), the recipient can reenter while `stagedFungible` is still set. During that reentrancy they can call `depositFungible`, which relies on the staged state, and get a deposit recorded without actually performing a fresh token transfer. This does not apply to the native-asset path because `_getStagedFungibleAndAmount` uses `msg.value`.

**Impact:** With standard ERC-20s there’s no issue. If a callback-capable token were ever used, reentrancy during `transfer` could:
* observe or reuse stale staged state
* record a `depositFungible` without an accompanying transfer, causing accounting discrepancy and potential value loss.

**Recommended mitigation:**
Follow checks-effects-interactions: clear the transient staged state before any external calls in `exchangeFungible`:
```diff
    (Fungible fungibleIn, uint256 amountIn) = _getStagedFungibleAndAmount();
    uint256 amountOut;

+   assembly ("memory-safe") {
+       // clear staged fungible
+       tstore(stagedFungible.slot, 0)
+   }

    // ...

    assembly ("memory-safe") {
        // clear staged fungible
-       tstore(stagedFungible.slot, 0)
```


**Licredity:** Fixed in [PR#62](https://github.com/Licredity/licredity-v1-core/pull/62/files), commit [`fb6a049`](https://github.com/Licredity/licredity-v1-core/commit/fb6a04925543aa77b873f0a1bdd86c7a22dba0f1)

**Cyfrin:** Verified. `stagedFungible` now cleared before external call.
