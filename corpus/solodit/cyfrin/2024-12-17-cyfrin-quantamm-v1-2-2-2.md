---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-2-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Extreme weight ratios combined with large balances can cause denial-of-service
  for unbalanced liquidity operations
vuln_class: []
---

# Extreme weight ratios combined with large balances can cause denial-of-service for unbalanced liquidity operations

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** The weighted pool math can potentially overflow when making unbalanced liquidity adjustments to a pool tokens with very small weights and large balances.

The issue occurs in `WeightedMath::computeBalanceOutGivenInvariant`:

```solidity
 newBalance = oldBalance * (invariantRatio ^ (1/weight))
```

When weights are small and invariant ratio is close to the maximum value (300%), even realistic balance changes can cause computations to overflow.

An example here taken from the fuzz test:

```solidity
// Balance computation scenario:
balance = 7500e21  (7.5 million tokens)
weight = 0.01166 (1.166%) // Just above absoluteWeightGuardRail minimum of 1% proposed for Balancer pools
invariantRatio = 3.0 // maximum value

calculation = 7500e21 * (3.0 ^ (1/0.01166))
           = 7500e21 * (3.0 ^ 85.76)
           = OVERFLOW
```

`QuantAMMWeightedPool` allows weights down to `0.1 %`, as seen in `QuantAMMWeightedPool::_setRule`:
```solidity
//applied both as a max (1 - x) and a min, so it cant be more than 0.49 or less than 0.01
//all pool logic assumes that absolute guard rail is already stored as an 18dp int256
require(
    int256(uint256(_poolSettings.absoluteWeightGuardRail)) <
        PRBMathSD59x18.fromInt(1) / int256(uint256((_initialWeights.length))) &&
        int256(uint256(_poolSettings.absoluteWeightGuardRail)) > 0.001e18, // @audit minimum guard rail allowed is 0.1 %
    "INV_ABSWGT"
); //Invalid absoluteWeightGuardRail value
```

**Impact:** Liquidity operations can revert for tokens with small weights and large balances. As a consequence, pool can become temporarily unusable as weights approach guard rail minimums. It is worth highlighting that users can always choose to proportionately add/remove liquidity to mitigate this scenario.

**Recommended Mitigation:** Risk of overflow exists when the minimum weight can go up to 1%. Even a modest increase of minimum weight to 3% effectively prevents this scenario. Consider changing the lowest enforced guard rail to be higher.

**QuantAMM:** Response from the balancer team and we agree:

> computeBalance is only used for unbalanced liquidity ops (add single token exact out, or remove single token exact in).
Add exact out is only used in batch swaps. Remove exact in could be used if you want to exit single sided I guess.
But in any case you can always exit proportional

> The example above uses an invariant ratio of 3, which is an add liquidity (>1). Compute balance for that ratio only happens for add single token exact out. You won't ever use that one unless you nest your pools (which is not supported anyways by default for [quantamm] weighted pools).

1% enforced as lowest guard rail in [`4beffda`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/4beffda73e0c38b9dc719d78147c06f1d59644bd)

**Cyfrin:** Verified.

\clearpage
