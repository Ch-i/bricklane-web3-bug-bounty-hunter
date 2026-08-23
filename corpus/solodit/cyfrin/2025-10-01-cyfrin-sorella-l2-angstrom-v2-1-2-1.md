---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-01-cyfrin-sorella-l2-angstrom-v2-1-2-1
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
title: '`TickIterator::_advanceToNextUp` sets uninitialized end tick as the current
  tick which causes `TickIterator::hasNext` to return true when this is not actually
  the case'
vuln_class: []
---

# `TickIterator::_advanceToNextUp` sets uninitialized end tick as the current tick which causes `TickIterator::hasNext` to return true when this is not actually the case

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-01-cyfrin-sorella-l2-angstrom-v2.1.md)_

---

**Description:** `TickIterator::hasNext` returns true if there are more ticks to iterate, inclusive if the end tick, while `TickIterator::getNext` returns the next tick and advances the iterator:

```solidity
function hasNext(TickIteratorUp memory self) internal pure returns (bool) {
@>   return self.currentTick <= self.endTick;
}

function getNext(TickIteratorUp memory self) internal view returns (int24 tick) {
    if (!hasNext(self)) revert NoNext();
    tick = self.currentTick;
    _advanceToNextUp(self);
}
```

`TickIterator::_advanceToNextUp` intends to advance the upward tick iterator to the next initialized tick, setting it as the current tick. The do-while loop condition terminates once the end tick is reached; however, this logic incorrectly considers the end tick as the next tick even when it is not initialized:

```solidity
function _advanceToNextUp(TickIteratorUp memory self) private view {
    do {
        (int16 wordPos, uint8 bitPos) =
            TickLib.position(TickLib.compress(self.currentTick, self.tickSpacing) + 1);

        if (bitPos == 0) {
            self.currentWord = self.manager.getPoolBitmapInfo(self.poolId, wordPos);
        }

        bool initialized;
        (initialized, bitPos) = self.currentWord.nextBitPosGte(bitPos);
@>      self.currentTick = TickLib.toTick(wordPos, bitPos, self.tickSpacing);
@>      if (initialized) break;
@>  } while (self.currentTick < self.endTick);
```

Instead, the iterator should marked as exhausted by setting `self.currentTick = type(int24).max` and adding explicit validation within `hasNext()` which should also use an exclusive comparison operator instead.

**Impact:** Based on the below PoC, this does not appear to affect either the effective price calculation or crediting of rewards as all repeated evaluations yield zero and effectively act as a no-op, although this is not a guarantee that such impact does not exist.

**Proof of Concept:** The following tests should be added to `TickIterator.t.sol`:

```solidity
function test_iterateUp_phantomAtTopOfWordBoundary() public view {
    // No liquidity anywhere.

    int24 startTick = 2500;
    int24 endTick = 2550;
    TickIteratorUp memory iter =
        TickIteratorLib.initUp(manager, pid, TICK_SPACING, startTick, endTick);

    // Erroneously returns true - should be false with no initialized ticks up to boundary.
    bool hasNext = iter.hasNext();
    console2.log("iter.hasNext(): %s", hasNext);

    // Returns endTick even though it isn't initialized - should revert with NoNext().
    int24 tick = iter.getNext();
    console2.log("iter.getNext(): %s", tick);
    console2.log("endTick: %s", endTick);

    // Prove the returned tick is not initialized.
    (int16 wordPos, uint8 bitPos) = TickLib.position(TickLib.compress(tick, TICK_SPACING));
    uint256 word = IPoolManager(address(manager)).getPoolBitmapInfo(pid, wordPos);
    console2.log("isInitialized: %s", TickLib.isInitialized(word, bitPos));
}

function test_iterateDown_noPhantomAtBottomOfWordBoundary() public view {
    // No liquidity anywhere.

    int24 startTick = 50;
    int24 endTick = 0;

    TickIteratorDown memory iter =
        TickIteratorLib.initDown(manager, pid, TICK_SPACING, startTick, endTick);

    // Should be exhausted - no initialized ticks in (0, 50].
    assertFalse(iter.hasNext(), "Down iterator has a phantom next tick");
}
```

The following test should be added to `AngstromL2.t.sol` and run with `forge test --mt test_tickIteration --decode-internal -vvvv`:

```solidity
function test_tickIteration() public {
    PoolKey memory key = initializePool(address(token), 10, 2500);
    addLiquidity(key, 2500, 2540, 1e21);
    uint256 PRIORITY_FEE = 0.5 gwei;
    setPriorityFee(PRIORITY_FEE);

    router.swap(key, false, 1000e18, int24(2550).getSqrtPriceAtTick());
}
```

**Recommended Mitigation:** Modify the upward tick iterator functions such that `hasNext()` returns false when there are no further initialized ticks.

**Sorella Labs:** Fixed in commit [0d6d39e](https://github.com/SorellaLabs/l2-angstrom/commit/0d6d39ec7be2d9e151aa47e05a6c0dec4364b2a5).

**Cyfrin:** Verified. The do-while loop is now inclusive of the end tick such that the current tick advances beyond the end and `hasNext()` returns false.
