---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Unnecessary `_initialWeights` sum check
vuln_class: []
---

# Unnecessary `_initialWeights` sum check

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** When first initializing a `QuantAMMWeightedPool` the pool creator provides the initial weights. These initial weights should sum up to 1 (`1e18`). The issue is however that this is verified both in [`QuantAMMWeightedPool::_setRule`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L767-L778):
```solidity
int256 sumWeights;
for (uint i; i < _initialWeights.length; ) {
    sumWeights += int256(_initialWeights[i]);
    unchecked {
        ++i;
    }
}

require(
    sumWeights == 1e18, // 1 for int32 sum
    "SWGT!=1"
); //Initial weights must sum to 1
```
And in [`QuantAMMWeightedPool::_setInitialWeights`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L625-L644):
```solidity
int256 normalizedSum;
int256[] memory _weightsAndBlockMultiplier = new int256[](_weights.length * 2);
for (uint i; i < _weights.length; ) {
    if (_weights[i] < int256(uint256(absoluteWeightGuardRail))) {
        revert MinWeight();
    }

    _weightsAndBlockMultiplier[i] = _weights[i];
    normalizedSum += _weights[i];
    //Initially register pool with no movement, first update will come and set block multiplier.
    _weightsAndBlockMultiplier[i + _weights.length] = int256(0);
    unchecked {
        ++i;
    }
}

// Ensure that the normalized weights sum to ONE
if (uint256(normalizedSum) != FixedPoint.ONE) {
    revert NormalizedWeightInvariant();
}
```
Consider removing the check in `_setRule` as that function is for verifying the rules and also the check in `_setInitialWeights` is more thorough, as it also checks they adhere to the `absoluteWeightGuardRail` requirement.

**QuantAMM:** Fixed in [`6b891e8`](https://github.com/QuantAMMProtocol/QuantAMM-V1/pull/36/commits/6b891e877f8dc1ec50b562d744c5fbb7c5f70eef)

**Cyfrin:** Verified.

\clearpage
