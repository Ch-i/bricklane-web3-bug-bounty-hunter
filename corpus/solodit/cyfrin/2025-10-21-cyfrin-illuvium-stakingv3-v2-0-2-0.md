---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-2-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Unoptimised overflow check in `_assertFixedBpsCap`
vuln_class: []
---

# Unoptimised overflow check in `_assertFixedBpsCap`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Description:** In the `_assertFixedBpsCap()` function, the overflow check `if (totalBps > Constants.BPS_DENOMINATOR)` is performed inside the loop for each pool iteration. This causes unnecessary conditional evaluations on every iteration, increasing gas usage. The check only needs to be performed once after summing all relevant `bps` values.

**Recommended Mitigation:** Accumulate `totalBps` inside the loop, then perform the overflow check once after the loop:

```solidity
function _assertFixedBpsCap() internal view {
    uint256 totalBps;
    for (uint256 i; i < pools.length; i++) {
        Pool storage pool = pools[i];
        if (!pool.active || pool.mode != PoolMode.FixedBps) continue;
        totalBps += pool.bps;
    }
    if (totalBps > Constants.BPS_DENOMINATOR) {
        revert FixedBpsOverflow(totalBps);
    }
}
```

This reduces gas cost by eliminating unnecessary conditional checks inside the loop.

**Illuvium**:
Fixed in commit [5f273bc](https://github.com/0xKaizenLabs/staking-contracts-v3/commit/5f273bc8a196170162400c33a43efe2fb84f0013).

**Cyfrin**:
Verified.

\clearpage
