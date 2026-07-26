---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`RevenueCounter::setFeeCollector, syncStablecoinRevenue` underflow on non-monotonic
  collector'
vuln_class: []
---

# `RevenueCounter::setFeeCollector, syncStablecoinRevenue` underflow on non-monotonic collector

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Both `syncStablecoinRevenue` and `setFeeCollector` compute `delta = currentCumulative - lastSyncedCumulative`. In Solidity 0.8.x the subtraction reverts when the new collector reports a lower cumulative than the previous. The switch path inside `setFeeCollector` syncs the old collector before updating (`RevenueCounter.sol:99-107`), so a regression blocks even the collector replacement. Recovery requires a two-step path (`setFeeCollector(address(0))` first, then switch to the new one), which is not documented in any runbook.

**Spec-Intent Gap:**

`specs/GOVERNANCE.md` §Revenue Counter Mechanism describes the two update paths (`syncStablecoinRevenue` permissionless, `attestRevenue` governance) but does not prescribe behaviour for `setFeeCollector` rotation under a non-monotonic old collector. The rotation path exists precisely to recover from a compromised or misbehaving collector, so the underflow-revert behaviour blocks the recovery channel in exactly the scenario it is designed to handle.

**Impact:** Permanent DoS of the stablecoin revenue tracking path until a two-step governance action. Downstream `ArmadaWindDown`'s `recognizedRevenueUsd < revenueThreshold` check under-counts; `RevenueLock` release schedules stall.

**Recommended Mitigation:** Saturate at zero and unconditionally update `lastSyncedCumulative`, and document the zero-collector reset:

```solidity
uint256 delta = currentCumulative > lastSyncedCumulative
    ? currentCumulative - lastSyncedCumulative
    : 0;
lastSyncedCumulative = currentCumulative;
if (delta > 0) {
    recognizedRevenueUsd += delta * USDC_TO_USD_SCALE;
    emit RevenueUpdated(recognizedRevenueUsd, recognizedRevenueUsd - delta * USDC_TO_USD_SCALE);
}
```

**Armada:** Fixed in commit [04c4550](https://github.com/ship-armada/armada-poc/commit/04c45501adda15c2f774e1ce563b3ab807e92c83).

**Cyfrin:** Verified.
