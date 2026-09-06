---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-0-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Inconsistent `blockNumberDeadline` for forced transactions can lead to DoS
  newer forced transactions requests
vuln_class: []
---

# Inconsistent `blockNumberDeadline` for forced transactions can lead to DoS newer forced transactions requests

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** When submitting a forced transaction on L1, the contract calculates `blockNumberDeadline` using the next formula:
```solidity
    uint256 blockNumberDeadline;
    unchecked {
      /// @dev The computation uses 1s block time making block number and seconds interchangeable,
      ///      while the chain might currently differ at >1s, this gives additional inclusion time.
      blockNumberDeadline =
        currentFinalizedL2BlockNumber +
        block.timestamp -
        _lastFinalizedState.timestamp +
        L2_BLOCK_BUFFER;
    }
```

The problem is that the delta between `block.timestamp` & `_lastFinalizedState.timestamp` varies significantly depending on when the forced transaction is submitted relative to the most recent finalization.
This creates inconsistent deadlines for users:
- Just before a new block is finalized - **Longer deadline**:
`_lastFinalizedState.timestamp` is very close to `block.timestamp` → small delta → higherblockNumberDeadline (longer deadline)
- Just after a new block was finalized - **Shorter deadline**:
`_lastFinalizedState.timestamp` is significantly older than `block.timestamp` → large delta → lowerblockNumberDeadline (shorter deadline)

This means two users submitting a forced transaction at almost the same real-world time can receive very different deadlines, purely based on finalization timing luck.

The root cause of the problem stems from the fact that the formula is meant to treat block numbers and seconds interchangeably, which means, as if the block's production rate would be 1 per second, but this is not the case [in Linea, the current block rate is](https://lineascan.build/chart/blocktime) ~1 block every 2 seconds.

**Impact:** Deadline varies significantly depending on how recently a block was finalized:
- Forced tx sent right after finalization → shorter deadline
- Forced tx sent right before next finalization → longer deadline



**Proof of Concept:** The next example demonstrates the discrepancy in the deadlines. Assume the blocks are finalized every 10k seconds at a rate of 1 block every 2 seconds. (That means, during each finalization, 5k blocks will be finalized).

Current state on the rollup is as:
- `currentFinalizedL2BlockNumber` = 50_000
- `_lastFinalizedState.timestamp` = 90_000

The next finalization would update values to:
- `currentFinalizedL2BlockNumber` = 55_000
- `_lastFinalizedState.timestamp` = 100_000

Here is what happens to the deadline when a forced tx is submitted right before the next finalization occurs:

| forced tx | Approx. real time | Time since last finalized state | Finalized L2 block # | blockNumberDeadline |
|------|-------------------|---------------------------------|----------------------|---------------------|
| 1    | t ≈ 99,999 s      | ~9,999 s                        | 50,000               | **59,999**          |
| 2    | t ≈ 100,001 s     | ~1 s                            | 55,000               | **55,001**          |


This discrepancy can lead to a DoS from subsequent forced transaction requests, as the newest transaction would have a lower `blockNumberDeadline` than the last stored forced transaction; `Rollup::storeForcedTransaction` explicitly reverts execution.
```solidity
  function storeForcedTransaction(
    ...
  ) external payable virtual onlyRole(FORCED_TRANSACTION_SENDER_ROLE) {
    unchecked {
      ...

      uint256 forcedTransactionNumber = nextForcedTransactionNumber++;

    //@audit-info => deadline for previous forced tx must be beyond the block number deadline assigned for the newest forced transaction
      require(
        forcedTransactionL2BlockNumbers[forcedTransactionNumber - 1] < _blockNumberDeadline,
        ForcedTransactionExistsForBlockOrIsTooLow(_blockNumberDeadline)
      );

      forcedTransactionRollingHashes[forcedTransactionNumber] = _forcedTransactionRollingHash;
      forcedTransactionL2BlockNumbers[forcedTransactionNumber] = _blockNumberDeadline;

      ...
    }
  }

```

The table below shows the outcome of requesting forced transactions using the original example of this issue:
| Tx | Submitted `blockNumberDeadline` | Assigned `forcedTransactionNumber` | Previous deadline (index n-1) | Check (prev < new)     | Outcome  |
|----|----------------------------------|-------------------------------------|-------------------------------|------------------------|----------|
| 1  | **59,999**                       | 1                                   | 0 (default/not set)           | 0 < 59,999 → **yes**   | **Success** |
| 2  | **55,001**                       | 2                                   | 59,999                        | 59,999 < 55,001 → **no** | **Revert**  |


**Recommended Mitigation:** Consider refactoring the `blockNumberDeadline` formula to account for the actual L2 block rate.

**Linea:** Fixed in commit [8d9b0f](https://github.com/Consensys/linea-monorepo/pull/2298/changes/8d9b0f94afc0bbb7f498b068319a2f2844340544) && [05309](https://github.com/Consensys/linea-monorepo/pull/2298/changes/053093da2e7a86b99909fcbf096eb96bd8815f0a).

**Cyfrin:** Verified. The formula for calculating `blockNumberDeadline` now adjusts the elapsed time for the finalization period based on the L2 block rate. Now, the `blockNumberDeadline` is adjusted in the `ForcedTransactionGateway` to add a buffer in the edge case where the calculated `blockNumberDeadline` is lower than the last recorded deadline on the Rollup; This buffer mitigates the case when the L2 block rate production deviates from the `L2_BLOCK_DURATION_SECONDS`.

\clearpage
