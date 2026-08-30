---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Token Index error in `getNormalizedWeights` calculates incorrect weight leading
  to incorrect pool asset allocation
vuln_class: []
---

# Token Index error in `getNormalizedWeights` calculates incorrect weight leading to incorrect pool asset allocation

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** The `_getNormalizedWeights()` function in `QuantAMMWeightedPool.sol` contains a critical indexing error when handling multipliers for pools with more than 4 tokens. The error causes incorrect multiplier values to be used when calculating interpolated weights for tokens 4-7, potentially leading to severe asset allocation errors.

The issue occurs in the _getNormalizedWeights() function when handling the second storage slot for pools with more than 4 tokens:

```solidity
function _getNormalizedWeights() internal view virtual returns (uint256[] memory) {
    // ...
    uint256 tokenIndex = totalTokens;
    if (totalTokens > 4) {
        tokenIndex = 4;  // @audit Sets to 4 for first slot multipliers
    }

    // First slot handles correctly
    normalizedWeights[0] = calculateBlockNormalisedWeight(
        firstFourWeights[0],
        firstFourWeights[tokenIndex],  // Uses indices 4-7 for multipliers
        timeSinceLastUpdate
    );
    // ...

    // Second slot has indexing error
    if (totalTokens > 4) {
        tokenIndex -= 4;  // @audit Resets to 0, breaking multiplier indices
        int256[] memory secondFourWeights = quantAMMUnpack32(_normalizedSecondFourWeights);
        normalizedWeights[4] = calculateBlockNormalisedWeight(
            secondFourWeights[0],
            secondFourWeights[tokenIndex],  // @audit Uses wrong indices 0-3 for multipliers -> essentially weight and multiplier are same
            timeSinceLastUpdate
        );
        // ...
    }
}
```
When processing the second slot of tokens (indices 4-7):
- First tokenIndex is set to 4 if total tokens > 4
- tokenIndex is decremented by 4, resetting to 0
- For all subsequent weight calculations, the weight & multiplier are effectively the same

**Impact:**
- Incorrect weight calculations for tokens 4-7 in pools with more than 4 tokens
- Significant deviation from intended pool asset allocation ratios


**Recommended Mitigation:** When there are more than 4 tokens in the pool, do not decrement the tokenIndex by 4.

**QuantAMM:** Fixed in [`60815f2`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/60815f262748579cba99bafb640e7931d6f13c47)

**Cyfrin:** Verified
