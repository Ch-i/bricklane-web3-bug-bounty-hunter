---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-10-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md
tags:
- firm:cyfrin
- report:2025-10-01-cyfrin-sorella-l2-angstrom-v2-1
title: Dust due to rounding tax calculations will accumulate in `AngstromL2` and cannot
  be recovered
vuln_class: []
---

# Dust due to rounding tax calculations will accumulate in `AngstromL2` and cannot be recovered

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** The sum of rewards owed to positions can be less than the total tax amount due to rounding. While it is correct to round down these proportional share calculations, any dust that is not accounted to `unclaimedProtocolRevenueInEther` will remain locked in the `AngstromL2` contract.

There does exist some logic to distribute the remainder of `taxInEther` to the last range; however, `rewardGrowthOutsideX128` is never incremented for the relevant tick:

```solidity
// Distribute remainder to last range and update global accumulator.
unchecked {
    cumulativeGrowthX128 += PoolRewardsLib.getGrowthDelta(taxInEther, liquidity);
    rewards[ticks.poolId].globalGrowthX128 += cumulativeGrowthX128;
}
```

Additionally, when the liquidity is zero then a zero growth delta is returned and the remainder would not be accounted anyway.

**Impact:** Dust amounts will accumulate and not be recoverable.

**Proof of Concept:** The following test should be added to `AngstromL2.t.sol`:

```solidity
function test_rewardDust() public {
    PoolKey memory key = initializePool(address(token), 10, 3);

    uint256 PRIORITY_FEE = 10 gwei;
    setPriorityFee(PRIORITY_FEE);
    uint256 tax = angstrom.getSwapTaxAmount(PRIORITY_FEE);

    int24[2][] memory positions = new int24[2][](3);
    positions[0] = [int24(0), int24(10)];
    positions[1] = [int24(10), int24(20)];
    positions[2] = [int24(20), int24(30)];

    for (uint256 i = 0; i < positions.length; i++) {
        addLiquidity(key, positions[i][0], positions[i][1], 1e22);
    }

    router.swap(key, false, 1000e18, int24(25).getSqrtPriceAtTick());

    uint256 cumulativeRewards;

    for (uint256 i = 0; i < positions.length; i++) {
        cumulativeRewards += angstrom.getPendingPositionRewards(
            key, address(router), positions[i][0], positions[i][1], bytes32(0)
        );
    }

    assertEq(cumulativeRewards, tax, "All tax should be rewarded/accounted");
}
```

**Recommended Mitigation:** Account any dust tax amounts to the `unclaimedProtocolRevenueInEther` state so that it can be withdrawn by the protocol.

**Sorella Labs:** Acknowledged. By definition it's dust so complexity of accounting that likely not worth the attack surface considering the value lost is likely not even worth the gas to account for it.

**Cyfrin:** Acknowledged.

\clearpage
