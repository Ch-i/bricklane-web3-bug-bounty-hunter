---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`ArmadaWindDown::triggerWindDown` can permissionlessly initiate wind-down
  even when revenue target has been met'
vuln_class: []
---

# `ArmadaWindDown::triggerWindDown` can permissionlessly initiate wind-down even when revenue target has been met

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `RevenueCounter::syncStablecoinRevenue` must be called to sync `RevenueCounter::recognizedRevenueUsd` - important protocol decisions should not be made prior to calling `syncStablecoinRevenue` since they could be processed using a stale revenue figure.

`ArmadaWindDown::triggerWindDown` calls `RevenueCounter::recognizedRevenueUsd` without first calling `syncStablecoinRevenue` to sync the revenue, then triggers the wind-down if enough time has elapsed and the revenue is insufficient:
```solidity
function triggerWindDown() external {
    require(!triggered, "ArmadaWindDown: already triggered");
    require(block.timestamp > windDownDeadline, "ArmadaWindDown: deadline not passed");
    require(
        // @audit no revenue sync, uses stale figure
        revenueCounter.recognizedRevenueUsd() < revenueThreshold,
        "ArmadaWindDown: revenue meets threshold"
    );
    _executeWindDown();
}
```

**Impact:** Wind-down can be permissionlessly triggered even though the actual revenue target has been met.

**Recommended Mitigation:** In `ArmadaWindDown::triggerWindDown` call `RevenueCounter::syncStablecoinRevenue` before reading `recognizedRevenueUsd`. Consider changing `syncStablecoinRevenue` to return the updated `recognizedRevenueUsd` to save the additional external call and storage read.

Alternatively if there is a risk that `syncStablecoinRevenue` will revert and block the wind-down, consider a solution such as:
```diff
function triggerWindDown() external {
    require(!triggered, "ArmadaWindDown: already triggered");
    require(block.timestamp > windDownDeadline, "ArmadaWindDown: deadline not passed");
+   try IRevenueCounterSync(address(revenueCounter)).syncStablecoinRevenue() {} catch {}
    require(
        revenueCounter.recognizedRevenueUsd() < revenueThreshold,
        "ArmadaWindDown: revenue meets threshold"
    );
    _executeWindDown();
}
```

**Armada:** Fixed in commit [09e4016](https://github.com/ship-armada/armada-poc/commit/09e40167ca73b549904a1bfd90f5467649f83469) using the alternative solution to prevent wind-down from being bricked if `syncStablecoinRevenue` reverts.

**Cyfrin:** Verified.
