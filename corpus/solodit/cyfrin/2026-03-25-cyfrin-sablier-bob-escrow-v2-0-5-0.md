---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-5-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Don't copy entire struct from `storage` to `memory` when only few fields required
vuln_class: []
---

# Don't copy entire struct from `storage` to `memory` when only few fields required

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Don't copy entire struct from `storage` to `memory` when only few fields required:

* `SablierBobState::_statusOf`
```diff
-        Bob.Vault memory vault = _vaults[vaultId];
+        Bob.Vault storage vault = _vaults[vaultId];
```

* `SablierEscrowState::_statusOf`
```solidity
    function _statusOf(uint256 orderId) internal view returns (Escrow.Status) {
        // @audit more efficient implementation
        // get storage reference
        Escrow.Order storage order = _orders[orderId];

        // 1 SLOAD
        (bool wasFilled, bool wasCanceled, uint40 expiryTime)
            = (order.wasFilled, order.wasCanceled, order.expiryTime);

        if (wasFilled) {
            return Escrow.Status.FILLED;
        }
        if (wasCanceled) {
            return Escrow.Status.CANCELLED;
        }

        // Return EXPIRED if the order has an expiry timestamp and it has expired.
        if (expiryTime != 0 && block.timestamp >= expiryTime) {
            return Escrow.Status.EXPIRED;
        }

        return Escrow.Status.OPEN;
    }
```

* `SablierEscrow::cancelOrder` - similar improvements to the previous by getting a `storage` reference then loading the first slot in 1 SLOAD

* `SablierEscrow::fillOrder` - potentially also better to use a `storage` reference then only read from storage required slots, to prevent duplicating storage reads already done inside the call to `_statusOf`

* `SablierBob::enter` - only needs `vault.adapter, vault.token, vault.shareToken`

**Sablier:** Fixed in commits [bc5d883](https://github.com/sablier-labs/lockup/commit/bc5d8839130b07cecaff64df591bc27fdbd8f374), [48f25c4](https://github.com/sablier-labs/lockup/commit/48f25c4c99a304b016650c5e2cdeda3bd96647bd), [PR1444](https://github.com/sablier-labs/lockup/pull/1444/changes).

**Cyfrin:** Verified; the fixes aren't exactly as recommended but still more efficient than the original implementations.
