---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-17-cyfrin-quantamm-v1-2-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md
tags:
- firm:cyfrin
- report:2024-12-17-cyfrin-quantamm-v1-2
title: Misconfigured index boundaries prevent certain swaps in QuantAMMWeightedPool
vuln_class: []
---

# Misconfigured index boundaries prevent certain swaps in QuantAMMWeightedPool

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-17-cyfrin-quantamm-v1.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-17-cyfrin-quantamm-v1.2.md)_

---

**Description:** Balancer pools can handle up to 8 tokens in weighted pools. QuantAMM uses this feature but optimizes storage by using only two slots. As a result, the first four tokens and the last four tokens are treated separately.

For swaps, this logic is implemented in [`QuantAMMWeightedPool::onSwap`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L242-L265):

```solidity
// if both tokens are within the first storage element
if (request.indexIn < 4 && request.indexOut < 4) {
    QuantAMMNormalisedTokenPair memory tokenWeights = _getNormalisedWeightPair(
        request.indexIn,
        request.indexOut,
        timeSinceLastUpdate,
        totalTokens
    );
    tokenInWeight = tokenWeights.firstTokenWeight;
    tokenOutWeight = tokenWeights.secondTokenWeight;
} else if (request.indexIn > 4 && request.indexOut < 4) {
    // if the tokens are in different storage elements
    QuantAMMNormalisedTokenPair memory tokenWeights = _getNormalisedWeightPair(
        request.indexOut,
        request.indexIn,
        timeSinceLastUpdate,
        totalTokens
    );
    tokenInWeight = tokenWeights.firstTokenWeight;
    tokenOutWeight = tokenWeights.secondTokenWeight;
} else {
    tokenInWeight = _getNormalizedWeight(request.indexIn, timeSinceLastUpdate, totalTokens);
    tokenOutWeight = _getNormalizedWeight(request.indexOut, timeSinceLastUpdate, totalTokens);
}
```

The issue arises in the second `else if` block, which is intended to handle cases where both tokens are in the second slot. However, the condition `request.indexOut < 4` is incorrect; it should be `request.indexOut >= 4`. Consequently, in [`_getNormalisedWeightPair`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L305-L325), the code will revert:

```solidity
function _getNormalisedWeightPair(
    uint256 tokenIndexOne, // @audit indexOut
    uint256 tokenIndexTwo, // @audit indexIn
    // ...
) internal view virtual returns (QuantAMMNormalisedTokenPair memory) {
    uint256 firstTokenIndex = tokenIndexOne; // @audit indexOut
    uint256 secondTokenIndex = tokenIndexTwo; // @audit indexIn
    // ...
    if (tokenIndexTwo > 4) { // @audit indexIn will always be > 4 from the branch above
        firstTokenIndex = tokenIndexOne - 4; // @audit indexOut, must be < 4 hence underflow
        secondTokenIndex = tokenIndexTwo - 4;
        totalTokensInPacked -= 4;
        targetWrappedToken = _normalizedSecondFourWeights;
    } else {
```

Here, `tokenIndexOne - 4` will underflow due to the incorrect condition.

In [`QuantAMMWeightedPool::_getNormalizedWeight`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L370-L404), there is a similar issue where the condition `tokenIndex > 4` should be `tokenIndex >= 4`:

```solidity
if (tokenIndex > 4) { // @audit should be >=
    // get the index in the second storage element
    index = tokenIndex - 4;
    targetWrappedToken = _normalizedSecondFourWeights;
    tokenIndexInPacked -= 4;
} else {
    // @audit first slot
    if (totalTokens > 4) {
         tokenIndexInPacked = 4;
    }
    targetWrappedToken = _normalizedFirstFourWeights;
```

This causes a failure when fetching the multiplier in [`QuantAMMWeightedPool::_calculateCurrentBlockWeight`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L352-L368):

```solidity
int256 blockMultiplier = tokenWeights[tokenIndex + (tokensInTokenWeights)];
```

In this case, `tokenWeights` contains 8 entries, but `tokenIndex + (tokensInTokenWeights)` equals 8, causing an array out-of-bounds error.

The same issue is also present in the following locations, though they currently have no impact:

- In [`QuantAMMWeightedPool::onSwap`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L252):
  ```solidity
  } else if (request.indexIn > 4 && request.indexOut < 4) { // @audit should be >=
  ```

- In [`QuantAMMWeightedPool::_getNormalisedWeightPair`](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L320):
  ```solidity
  if (tokenIndexTwo > 4) { // @audit should be >=
  ```

**Impact:**
1. Swaps where `indexIn > 4` and `indexOut < 4` are impossible.
2. Swaps involving token index 4 cannot be performed.
3. If swaps with `indexIn > 4` and `indexOut < 4` would be possible, the swap amounts would be calculated incorrectly.

**Proof of Concept:** Add the following tests to `pkg/pool-quantamm/test/foundry/QuantAMMWeightedPool8Token.t.sol` to demonstrate the issues:
```solidity
// cross swap not working correctly
function testGetNormalizedWeightOnSwapOutGivenInNBlocksAfterToken7Token3() public {
    testParam memory firstWeight = testParam(7, 0.1e18, 0.001e18); // indexIn > 4
    testParam memory secondWeight = testParam(3, 0.15e18, 0.001e18); // indexOut < 4
    // will revert on underflow
    _onSwapOutGivenInInternal(firstWeight, secondWeight, 2, 1.006410772600252500e18);
}
// index >= 4 not working correctly
function testGetNormalizedWeightOnSwapOutGivenInInitialToken0Token4() public {
    testParam memory firstWeight = testParam(0, 0.1e18, 0.001e18);
    testParam memory secondWeight = testParam(4, 0.15e18, 0.001e18);
    // fails with `panic: array out-of-bounds access`
    _onSwapOutGivenInInternal(firstWeight, secondWeight, 0, 0.499583703357018000e18);
}
// index >= 4 not working correctly
function testGetNormalizedWeightOnSwapOutGivenInInitialToken4Token0() public {
    testParam memory firstWeight = testParam(4, 0.1e18, 0.001e18);
    testParam memory secondWeight = testParam(0, 0.15e18, 0.001e18);
    // fails with `panic: array out-of-bounds access`
    _onSwapOutGivenInInternal(firstWeight, secondWeight, 0, 0.887902403682279000e18);
}
```

**Recommended Mitigation:**
1. **Refactor the `if` block** in `QuantAMMWeightedPool::onSwap` as follows:

   ```solidity
   if (request.indexIn < 4 && request.indexOut < 4 || request.indexIn >= 4 && request.indexOut >= 4) {
       // Same slot; _getNormalisedWeightPair handles the correct logic
       tokenWeights = _getNormalisedWeightPair(...);
   } else {
       // Cross-slot handling
       tokenWeights = _getNormalizedWeight(...);
   }
   ```

2. **Update** conditions `> 4` to `>= 4` at the following lines:

   - [Line 320](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L320)
   - [Line 383](https://github.com/QuantAMMProtocol/QuantAMM-V1/blob/7213401491f6a8fd1fcc1cf4763b15b5da355f1c/pkg/pool-quantamm/contracts/QuantAMMWeightedPool.sol#L383)

**QuantAmm:**
Fixed in [`414d4bc`](https://github.com/QuantAMMProtocol/QuantAMM-V1/commit/414d4bc3d8699f1e4620f0060226b4e23ff3b010)

**Cyfrin:** Verfied.
