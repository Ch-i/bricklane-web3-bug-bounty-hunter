---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-0-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Incorrect handling of negative multipliers in `QuantAMMWeightedPool` leads
  to underflow in weight calculation
vuln_class: []
---

# Incorrect handling of negative multipliers in `QuantAMMWeightedPool` leads to underflow in weight calculation

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** In [`QuantAMMWeightedPool::calculateBlockNormalisedWeight`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L505-L521):
```solidity
if (multiplier > 0) {
    return uint256(weight) + FixedPoint.mulDown(uint256(multiplierScaled18), timeSinceLastUpdate);
} else {
    // @audit silent overflow, uint256(multiplierScaled18) of a negative value will result in a very large value
    return uint256(weight) - FixedPoint.mulUp(uint256(multiplierScaled18), timeSinceLastUpdate);
}
```

**Impact:** All swaps with negative multiplier which aren't on the same block that the update happened (`timeSinceLastUpdate != 0`) will fail due to underflow.

**Proof of Concept:** Add the following test to `pkg/pool-quantamm/test/foundry/QuantAMMWeightedPool8Token.t.sol`:
```solidity
function testGetNormalizeNegativeMultiplierOnSwapOutGivenInInitialToken0Token1() public {
    testParam memory firstWeight = testParam(0, 0.1e18, 0.001e18);
    testParam memory secondWeight = testParam(1, 0.15e18, -0.001e18);
    _onSwapOutGivenInInternal(firstWeight, secondWeight, 2, 1.332223208952048000e18);
}
```

**Recommended Mitigation:** Consider multiplying by `-1` first:
```diff
- return uint256(weight) - FixedPoint.mulUp(uint256(multiplierScaled18), timeSinceLastUpdate);
+ return uint256(weight) - FixedPoint.mulUp(uint256(-multiplierScaled18), timeSinceLastUpdate);
```

**QuantAMM:** Fixed in commit [`31636cf`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/31636cf736e9f6eda09f569bceb4e8d9bd3137bb)

**Cyfrin:** Verified.
