---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-03-19-cyfrin-linea-spingame-v2-0-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-19T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md
tags:
- firm:cyfrin
- report:2025-03-19-cyfrin-linea-spingame-v2-0
title: Rounding errors in boosted probability calculation can cause guaranteed wins
  to fail
vuln_class: []
---

# Rounding errors in boosted probability calculation can cause guaranteed wins to fail

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-03-19-cyfrin-linea-spingame-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-03-19-cyfrin-linea-spingame-v2.0.md)_

---

**Description:** The Linea SpinGame includes a boosting feature that allows the protocol to increase a specific user's chance of winning. However, this mechanism introduces the possibility of a user's total winning probability exceeding 100%, as the boosted probabilities can sum to a value greater than 100%. To address this, the contract normalizes the total boosted probability in [`Spin::_fulfillRandomness`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L538-L557):

```solidity
// Apply boost on the sum of totalProbabilities.
uint256 boostedTotalProbabilities = totalProbabilities * userBoost / BASE_POINT;

// If boostedTotalProbabilities exceeds 100% we have to increase the winning threshold so it stays in bound.
//
// Example:
//   PrizeA probability: 50%
//   PrizeB probability: 30%
//   User boost: 1.5x
//   boostedPrizeAProbability: 75%
//   boostedPrizeBProbability: 45%
//
//   We now have a total of 120% totalBoostedProbability so we need to increase winning threshold by boostedTotalProbabilities to BASE_POINT ratio.
//
//   winningThreshold = winningThreshold * 12_000 / 10_000
if (boostedTotalProbabilities > BASE_POINT) {
    winningThreshold =
        (winningThreshold * boostedTotalProbabilities) /
        BASE_POINT;
}
```

Later in [`Spin::_fulfillRandomness`](https://github.com/Consensys/linea-hub/blob/295344925ec4321265f7cbac174fcf903b529a4e/contracts/src/Spin.sol#L569-L589), each prize probability is independently scaled when checking if the user has won:

```solidity
// Apply boost on a single prize probability.
uint256 boostedPrizeProbability = prizeProbability * userBoost / BASE_POINT;

unchecked {
    cumulativeProbability += boostedPrizeProbability;
}

if (winningThreshold < cumulativeProbability) {
    selectedPrizeId = localPrizeIds[i];

    // ... win
    break;
}
```

The issue arises from the probability calculation:

```solidity
uint256 boostedPrizeProbability = prize.probability +
    ((prize.probability * userBoost) / BASE_POINT);
```

Due to this calculation, the final `cumulativeProbability` can be lower than `boostedTotalProbabilities`, leading to a scenario where a user who should be guaranteed a win might still lose due to rounding errors.

**Impact:** A user who theoretically has a 100% chance of winning can still lose. While this is an unlikely edge case, it would be highly problematic for the unlucky user who, despite the math suggesting they are guaranteed a win, does not receive a prize due to numerical precision issues.

**Proof of Concept:** Consider the following example:

- There are three prizes, each with a 30% probability of being won.
- A user receives a 133% probability boost.

Calculating the boosted probabilities:

```solidity
boostedTotalProbabilities = 0.9e8*133_333_333/1e8 = 119_999_999
boostedPrizeProbability = 0.3e8*133_333_333/1e8 = 39_999_999
```
and
```
3*39_999_999 = 119_999_997
```

In the worst case, the user could get:

```
winningThreshold = 99_999_999
```

Applying the threshold adjustment:

```solidity
if (boostedTotalProbabilities > BASE_POINT) {
    winningThreshold =
        (winningThreshold * boostedTotalProbabilities) /
        BASE_POINT;
}
```

This results in:

```
winningThreshold = 99_999_999 * 119_999_999 / 1e8 = 119_999_997
```

Since `winningThreshold < cumulativeProbability` is the condition for winning, and:

```
119_999_997 < 119_999_997  // (false)
```

The condition fails, meaning the user loses, even though they were supposed to be guaranteed a win. This issue is caused by the rounding errors in scaling probabilities.


**Recommended Mitigation:** Consider ensuring that in the last iteration of the loop, if `boostedTotalProbabilities >= BASE_POINT`, the user is guaranteed a win:

```diff
- if (winningThreshold < cumulativeProbability) {
+ if (winningThreshold < cumulativeProbability ||
+     boostedTotalProbabilities >= BASE_POINT && i == prizeLen - 1 // last iteration and win is guaranteed
+ ) {
      selectedPrizeID = prizeIds[i];
```

This change slightly favors the last prize in the list in extremely rare cases, but given that this situation is already highly improbable, this trade-off is reasonable.

**Linea:** Fixed in commit [`b32e038`](https://github.com/Consensys/linea-hub/commit/b32e038bba336d1ad6dddbdb972de8cafbbb2c1a)

**Cyfrin:** Verified.
