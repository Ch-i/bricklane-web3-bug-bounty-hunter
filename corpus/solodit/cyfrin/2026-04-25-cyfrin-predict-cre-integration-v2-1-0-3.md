---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-04-25-cyfrin-predict-cre-integration-v2-1-0-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-04-25T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md
tags:
- firm:cyfrin
- report:2026-04-25-cyfrin-predict-cre-integration-v2-1
title: Stuck round when `isEnabled == false` and last pre-created round closes
vuln_class: []
---

# Stuck round when `isEnabled == false` and last pre-created round closes

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-04-25-cyfrin-predict-cre-integration-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-04-25-cyfrin-predict-cre-integration-v2.1.md)_

---

**Description:** When `disableRoundConfig` is called, it sets `roundConfig.isEnabled = false` but leaves `currentRoundStartTimestamp` and `latestRoundStartTimestamp` unchanged. The Chainlink CRE offchain workflow (`readRoundConfigs.ts`) only reads `currentRoundStartTimestamp` to decide which rounds to close — it never reads or checks `isEnabled`. As a result, the CRE keeps submitting close-round reports for a disabled config exactly as if it were active.

The critical failure occurs when the CRE closes the last pre-created round of a disabled config (the one at `latestRoundStartTimestamp`). At that point, inside `_closeRound`:

```solidity
function _closeRound(bytes32 feedId, uint32 interval, uint32 startTimestamp, int192 endPrice) private {
    ...

    uint32 nextRoundStartTimestamp = startTimestamp + interval;
    bool present = _setNextRoundStartPriceIfPresent(feedId, nextRoundStartTimestamp, interval, endPrice);
    if (present) {
        roundConfig.currentRoundStartTimestamp = nextRoundStartTimestamp;
    }
    if (roundConfig.isEnabled) {
        uint32 newLatestTimestamp = roundConfig.latestRoundStartTimestamp + interval;
        roundConfig.latestRoundStartTimestamp = newLatestTimestamp;
        _createRound(feedId, newLatestTimestamp, interval);
    }
}
```

Because `isEnabled = false`, no next round was ever pre-created, so `_setNextRoundStartPriceIfPresent` returns `false`, and `currentRoundStartTimestamp` is never advanced. It permanently points to the round that was just resolved.

The CRE offchain workflow reads the on-chain state in `readRoundConfigs.ts` through two Multicall3 batches. Batch 1 fetches `roundConfigIndices` (unchanged by disable), batch 2 fetches `roundConfigs` by key and decodes the result — but only extracts `currentRoundStartTimestamp`, the first field of the struct. `isEnabled` is never read:

```typescript
// readRoundConfigs.ts — Batch 1: read roundConfigIndices (unchanged after disable)
indexCalls.push({
  target: adapterAddress,
  allowFailure: false,
  callData: encodeFunctionData({
    abi: ChainlinkUpDownAdapter,
    functionName: "roundConfigIndices",
    args: [feedId, interval],
  }),
});

// ...

// Batch 2: read roundConfigs by key
configCalls.push({
  target: adapterAddress,
  allowFailure: false,
  callData: encodeFunctionData({
    abi: ChainlinkUpDownAdapter,
    functionName: "roundConfigs",
    args: [key],
  }),
});

// ...

// Only currentRoundStartTimestamp is decoded — isEnabled is never read
const [currentRoundStartTimestamp] = decoded;
return { feedId, interval, currentRoundStartTimestamp: BigInt(currentRoundStartTimestamp) };
```

Back in `onCronTrigger.ts`, the only two guards applied to the returned timestamps are a zero-check and a time check. A disabled config satisfies both, so it is treated identically to an active one:

```typescript
// onCronTrigger.ts — Step 2: filter ready rounds
for (const { feedId, interval, currentRoundStartTimestamp } of roundTimestamps) {
  if (currentRoundStartTimestamp === 0n) {       // guard 1: not initialized
    runtime.log(`${feedId} / ${interval}s not initialized, skipping`);
    continue;
  }

  const roundEndTimestamp = currentRoundStartTimestamp + BigInt(interval);
  if (nowSeconds < roundEndTimestamp) {           // guard 2: not ended yet
    runtime.log(`${feedId} / ${interval}s round not ended yet, skipping`);
    continue;
  }
}
```

When submitting the transaction, `_processReport` calls `_closeRound`, which calls `_resolveQuestion`, which calls `CTF.reportPayouts` on an already-resolved condition:

```solidity
require(payoutDenominator[conditionId] == 0, "payout denominator already set");
```

This reverts on every attempt, indefinitely. Only `enableRoundConfig` (admin) recovers — but the M-5 issue can brick that path at historically-used boundaries, composing to a permanent lock.

**Impact:** The stuck disabled config poisons the entire CRE batch. `onCronTrigger.ts` collects all ready rounds across every configured `feedId`/`interval` pair and submits them in a single on-chain call via `writeCloseRounds`. Since there is no per-report error isolation in `_processReport` (line 245 of `ChainlinkUpDownAdapter.sol`) — the whole batch reverts — every invocation reverts, blocking all valid rounds across all other feeds from ever being settled. User funds in every active market are frozen indefinitely until the admin manually calls `enableRoundConfig` to recover the stuck config.

Direct violation of client concern 1 ("rounds are never stuck").

**Recommended Mitigation:** Advance `currentRoundStartTimestamp` to `0` when the last pre-created round closes with `isEnabled = false`. Setting `currentRoundStartTimestamp = 0` causes the CRE's existing guard (`if (currentRoundStartTimestamp === 0n) continue`) to skip this pair on every subsequent tick without any offchain changes. Alternatively, modify the offchain infrastructure to read and respect `isEnabled`.

**Predict.fun:** Fixed in commit [c608ae](https://github.com/PredictDotFun/prediction-market/commit/c608aeb561fad4c9ef1c8c2070eae43fdc6f0f2f)

**Cyfrin:** Verified.
