---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-21-cyfrin-illuvium-stakingv3-v2-0-0-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-21T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-21-cyfrin-illuvium-stakingv3-v2-0
title: Reserve-weighted allocations use spot reserves
vuln_class: []
---

# Reserve-weighted allocations use spot reserves

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-21-cyfrin-illuvium-stakingv3-v2.0.md)_

---

**Finding (Low): Reserve-weighted allocation uses spot reserves → price-manipulable**

**Description:** [`L2RevenueDistributorV3::_computeReserveUnits`](https://github.com/0xKaizenLabs/staking-contracts-v3/blob/c78653ed5f2e5a6d5ace13c303a8765fe30679b0/src/L2RevenueDistributorV3.sol#L521-L525) derives LP “units” from the current pair reserves (`getReserves()` and `totalSupply()`), i.e., a spot snapshot:
```solidity
IAerodromePair pair = IAerodromePair(pairAddr);
(uint256 r0, uint256 r1,) = pair.getReserves();
address t0 = pair.token0();
address t1 = pair.token1();
uint256 ilvReserve = t0 == address(ilv) ? r0 : (t1 == address(ilv) ? r1 : 0);
```
This allows for manipulation of the reserves.

**Impact:** A caller can briefly skew LP reserves right before `distribute` to steer that call’s rewards toward a chosen LP vault. The cost is a temporary trade + fees; repeating the tactic can compound gains. Base’s lack of a public mempool reduces public MEV but doesn’t eliminate manipulation completely.

**Recommended Mitigation:** Consider using a TWAP of reserves over a fixed window from the pair’s `observations`. Revert if the oracle history cannot satisfy the requested window. Sufficient observation length can be guaranteed by the protocol when deploying the pool.

```solidity
// Extend the pair interface as needed for your Aerodrome build.
interface IAerodromePairOracle is IAerodromePair {
    function observationLength() external view returns (uint256);
    function lastObservation()
        external
        view
        returns (uint256 timestamp, uint256 reserve0Cumulative, uint256 reserve1Cumulative);
    function observations(uint256 index)
        external
        view
        returns (uint256 timestamp, uint256 reserve0Cumulative, uint256 reserve1Cumulative);
}

library OracleLib {
    error OracleInsufficientHistory(); // fewer than 2 observations
    error OracleWindowNotSatisfied(uint256 availableWindow, uint256 requiredWindow);

    /// @dev Returns average reserves over `windowSecs` using cumulative reserve observations.
    function averageReserves(address pairAddr, uint32 windowSecs)
        internal
        view
        returns (uint256 avgR0, uint256 avgR1)
    {
        IAerodromePairOracle pair = IAerodromePairOracle(pairAddr);
        uint256 len = pair.observationLength();
        if (len < 2) revert OracleInsufficientHistory();

        (uint256 tNew, uint256 r0New, uint256 r1New) = pair.lastObservation();
        uint256 tTarget = tNew - uint256(windowSecs);

        // Walk back to an observation at or before tTarget (use binary search if ring buffer is large).
        uint256 idx = len - 2;
        (uint256 tOld, uint256 r0Old, uint256 r1Old) = pair.observations(idx);
        while (tOld > tTarget) {
            if (idx == 0) {
                revert OracleWindowNotSatisfied(tNew - tOld, windowSecs);
            }
            idx--;
            (tOld, r0Old, r1Old) = pair.observations(idx);
        }

        uint256 dt = tNew - tOld;
        if (dt == 0) revert OracleWindowNotSatisfied(0, windowSecs);

        avgR0 = (r0New - r0Old) / dt;
        avgR1 = (r1New - r1Old) / dt;
    }
}

contract L2RevenueDistributorV3 {
    // ...
    uint32 internal constant TWAP_WINDOW = 15 minutes;

    function _computeReserveUnits(Pool storage pool) internal view returns (uint256) {
        if (pool.kind != PoolKind.Vault) return 0;

        // ILV single-asset vault unchanged
        if (pool.underlyingToken == address(ilv)) {
            return IStakingVaultMinimal(pool.recipient).totalStaked();
        }

        // LP vault: use TWAP average reserves; revert if oracle history is insufficient
        address pairAddr = pool.underlyingToken;
        if (pairAddr == address(0)) return 0;

        (uint256 avgR0, uint256 avgR1) = OracleLib.averageReserves(pairAddr, TWAP_WINDOW);

        IAerodromePair p = IAerodromePair(pairAddr);
        address t0 = p.token0();
        address t1 = p.token1();
        uint256 ilvReserveAvg = t0 == address(ilv) ? avgR0 : (t1 == address(ilv) ? avgR1 : 0);
        if (ilvReserveAvg == 0) return 0;

        uint256 lpSupply = p.totalSupply();
        if (lpSupply == 0) return 0;

        uint256 vaultLp = IStakingVaultMinimal(pool.recipient).totalStaked();
        return (ilvReserveAvg * vaultLp) / lpSupply;
    }
}
```

**Illuvium:** Acknowledged; Reserve weighted pool allocations will stay using spot reserves from Aerodrome pairs. We'll use reasonable slippage protection params to ensure frontrunning isn't profitable/feasible + count with Base's trusted sequencer.
