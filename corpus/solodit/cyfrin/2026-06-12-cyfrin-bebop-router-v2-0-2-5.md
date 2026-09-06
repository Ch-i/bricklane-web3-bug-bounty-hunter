---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_calculateAmounts` applies oracle and checker fee and slippage
  rates with no upper bound, risking division-by-zero and underflow at or above `UNIT_BASE`'
vuln_class: []
---

# `BebopRouter::_calculateAmounts` applies oracle and checker fee and slippage rates with no upper bound, risking division-by-zero and underflow at or above `UNIT_BASE`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_getFeeAndSlippage` returns the raw `uint256` values from `IChecker::checkAndGetFee` and `IOracle::getSlippage` with no validation against `UNIT_BASE` (1,000,000 = 100%). These values feed directly into `_calculateAmounts` without any prior bounds check.

In exactOut mode (lines 414-416), `combinedRate = fee + slippage` is used as `UNIT_BASE - combinedRate` in the denominator of the gross-up formula. When `combinedRate == UNIT_BASE`, the denominator is zero, causing an EVM division-by-zero revert. When `combinedRate > UNIT_BASE`, the subtraction `UNIT_BASE - combinedRate` underflows, also reverting. In exactIn mode (line 408) and balance-of-router mode (line 431), `toAmountAfterFeeSlippage = newToAmount - feeAmount - slippageAmount` underflows whenever `feeAmount + slippageAmount > newToAmount`, which occurs when `fee + slippage > UNIT_BASE`.

Even below `UNIT_BASE`, rates approaching 100% silently strip the receiver's output to near zero. There is no code-level cap protecting against a per-order oracle or checker returning an extreme rate.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_calculateAmounts` (lines 408, 414-416, 431)

**Impact:** A per-order oracle or checker that returns a combined rate at or above `UNIT_BASE` bricks every `swap` and `settle` call bound to that order with an opaque arithmetic revert. The affected orders are unfillable until the rate returns below 100% or the signer issues new orders with a different oracle/checker. Large-but-sub-`UNIT_BASE` rates silently transfer most of the receiver's expected output to the treasury and makers as fee/slippage, with no on-chain ceiling protecting the user. Recovery from the DoS case requires the oracle to self-correct or the signer to re-issue orders, so the path is recoverable but temporarily broken.

**Recommended Mitigation:** After fetching fee and slippage, add `require(fee + slippage < UNIT_BASE)` (and individually `fee <= UNIT_BASE`, `slippage <= UNIT_BASE`) before passing the rates to `_calculateAmounts`. Emit a typed error (e.g. `RateExceedsUnitBase`) so callers can distinguish this failure from arithmetic panics. Consider a protocol-level `MAX_COMBINED_RATE` constant as an additional defense-in-depth bound.

**Bebop:** Fixed in commit [9db95bc](https://github.com/bebop-dex/bebop-rfqa/commit/9db95bc2b423d9317c149e90a70ae51565e26367).

**Cyfrin:**
Verified.
