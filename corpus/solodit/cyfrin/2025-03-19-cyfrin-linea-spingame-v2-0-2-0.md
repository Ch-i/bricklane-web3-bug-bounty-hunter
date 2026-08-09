---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Scaling `winningThreshold` incorrectly reduces randomness distribution
vuln_class: []
---

# Scaling `winningThreshold` incorrectly reduces randomness distribution

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** When a user has a boost that results in a >100% probability of winning, the contract adjusts `winningThreshold` to match `boostedTotalProbabilities` in [`Spin::_fulfillRandomness`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L534-L557):

```solidity
uint256 winningThreshold = _randomness % BASE_POINT;

// ...

if (boostedTotalProbabilities > BASE_POINT) {
    winningThreshold =
        (winningThreshold * boostedTotalProbabilities) /
        BASE_POINT;
}
```

The issue here is that `_randomness` is first scaled down to `BASE_POINT` before being scaled up to `boostedTotalProbabilities`. This process reduces the effective randomness (entropy) because some values in the original `_randomness` range will no longer be represented in the final `winningThreshold` after scaling. As a result, the final threshold may not be evenly distributed, potentially introducing bias.

Consider applying `_randomness` directly to `boostedTotalProbabilities` when the win probability exceeds 100%, ensuring no loss of entropy:

```diff
  if (boostedTotalProbabilities > BASE_POINT) {
-     winningThreshold =
-         (winningThreshold * boostedTotalProbabilities) /
-         BASE_POINT;

+     winningThreshold = _randomness % boostedTotalProbabilities;
  }
```

This preserves the full randomness range and ensures a more uniform distribution of possible winning thresholds.

**Linea:** Fixed in commit [`37a18ca`](https://github.com/Consensys/linea-hub/commit/37a18ca60b8e503643b5b6e996e9a0cd7c257ec2)

**Cyfrin:** Verified.
