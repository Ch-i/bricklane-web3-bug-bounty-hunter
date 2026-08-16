---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-4-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Optimisation of elapsed epoch calculation
vuln_class: []
---

# Optimisation of elapsed epoch calculation

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** In the `UptimeTracker::computeValidatorUptime` function, there is an opportunity to optimize how the number of elapsed epochs is calculated.

```solidity
Currently, the code redundantly retrieves both epoch indices and their corresponding start timestamps to compute the elapsed time between epochs:

uint48 lastUptimeEpoch = l1Middleware.getEpochAtTs(uint48(lastUptimeCheckpoint.timestamp));
uint256 lastUptimeEpochStart = l1Middleware.getEpochStartTs(lastUptimeEpoch);

uint48 currentEpoch = l1Middleware.getEpochAtTs(uint48(block.timestamp));
uint256 currentEpochStart = l1Middleware.getEpochStartTs(currentEpoch);

uint256 elapsedTime = currentEpochStart - lastUptimeEpochStart;
uint256 elapsedEpochs = elapsedTime / epochDuration;
```

However, since the epoch numbers themselves are already known (lastUptimeEpoch and currentEpoch), the number of full epochs that have elapsed can be directly calculated by subtracting the epoch indices, avoiding the unnecessary calls to getEpochStartTs.

**Recommended Mitigation:** Replace the timestamp-based epoch duration calculation with a simpler and more efficient version:

```diff
- uint256 elapsedTime = currentEpochStart - lastUptimeEpochStart;
- uint256 elapsedEpochs = elapsedTime / epochDuration;
+ uint256 elapsedEpochs = currentEpoch - lastUptimeEpoch;
```

This change reduces computational overhead and simplifies the logic while achieving the same result.

**Suzaku:**
Fixed in commit [f9946ef](https://github.com/suzaku-network/suzaku-core/commit/f9946ef8f6c7d7ab946e01d906f411352004ee41).

**Cyfrin:** Verified.
