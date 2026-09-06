---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-14
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaCrowdfund::computeAllocation, computeAllocationAtHop` revert in `refundMode`,
  breaking spec''s "always returns theoretical entitlement" guarantee'
vuln_class: []
---

# `ArmadaCrowdfund::computeAllocation, computeAllocationAtHop` revert in `refundMode`, breaking spec's "always returns theoretical entitlement" guarantee

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `CROWDFUND.md:355` defines both views as: "always returns the theoretical entitlement regardless of timing or claim status. It is pure deterministic math over finalized state". `:645` directs the observer to "query on-chain finalized aggregate state through `computeAllocation()`".

`ArmadaCrowdfund::computeAllocation, computeAllocationAtHop` (`contracts/crowdfund/ArmadaCrowdfund.sol:644-645, 662-663`) reject the refund branch:

```solidity
require(phase == Phase.Finalized, "ArmadaCrowdfund: not finalized");
require(!refundMode, "ArmadaCrowdfund: sale in refund mode");
```

The pre-finalize gate is consistent with the spec qualifier "pure deterministic math over finalized state" (`finalCeilings` and `finalDemands` are zero pre-finalize, so the answer is genuinely undefined). The `!refundMode` gate is not consistent: in `refundMode` the entitlement is well-defined as `(armAmount: 0, refundUsdc: sum over hops of participants[addr][h].committed)`, and the spec's "regardless of timing or claim status" wording means the view should keep returning the same theoretical entitlement before and after `claimRefund`.

**Impact:** Observers and UIs that follow the spec's instruction to use `ArmadaCrowdfund::computeAllocation` as the canonical post-finalization view must special-case `refundMode` and read `participants[addr][h].committed` directly across all hops, defeating the canonical-view promise.

**Recommended Mitigation:** Drop the `!refundMode` require and have the views compute the refund-mode answer directly:

```diff
function computeAllocation(address addr) public view returns (
    uint256 armAmount,
    uint256 refundUsdc
) {
    require(phase == Phase.Finalized, "ArmadaCrowdfund: not finalized");
-   require(!refundMode, "ArmadaCrowdfund: sale in refund mode");
+   bool refundModeCache = refundMode;

    for (uint8 h; h < NUM_HOPS; h++) {
        Participant storage p = participants[addr][h];
        if (p.committed == 0) continue;

+       if (refundModeCache) {
+           refundUsdc += p.committed;
+           continue;
+       }
        (uint256 allocArm, , uint256 hopRefund) = _computeAllocation(p.committed, h, _effectiveCap(p, h));
        armAmount += allocArm;
        refundUsdc += hopRefund;
    }
}
```

Apply the equivalent change to `computeAllocationAtHop`.

**Armada:** Fixed in commit [eda2cee](https://github.com/ship-armada/armada-poc/commit/eda2ceeb9091f8ffd9ba93cd9a7f9244b3a8ede3).

**Cyfrin:** Verified.


\clearpage
