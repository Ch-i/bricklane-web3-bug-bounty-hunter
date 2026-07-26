---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-12-cyfrin-bebop-router-v2-0-2-16
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-06-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-12-cyfrin-bebop-router-v2-0
title: '`BebopRouter::_getFeeAndSlippage` passes full-quote PMM amounts to the oracle
  instead of the scaled actual fill, mispricing slippage on partial fills'
vuln_class: []
---

# `BebopRouter::_getFeeAndSlippage` passes full-quote PMM amounts to the oracle instead of the scaled actual fill, mispricing slippage on partial fills

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-12-cyfrin-bebop-router-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-12-cyfrin-bebop-router-v2.0.md)_

---

**Description:** `_validateAndPrepare` obtains the oracle slippage rate before calculating the current fill:

```solidity
// contracts/BebopRouter.sol:251-255
// Get fee/slippage + calculate amounts
{
    (ctx.feeValue, ctx.slippageValue) = _getFeeAndSlippage(order, extraInfo, ctx.pmm);
    ctx.calc = _calculateAmounts(exactAmount, order, ctx.feeValue, ctx.slippageValue);
}
```

`_getFeeAndSlippage` forwards the full PMM quote amounts decoded from the PMM calldata:

```solidity
// contracts/BebopRouter.sol:385-389
if (order.oracle != address(0)) {
    // Use actual PMM amounts from calldata (not order amounts, since calldata is replaceable)
    slippage = IOracle(order.oracle).getSlippage(
        order.pmmFromToken, order.pmmToToken, pmm.pmmTakerAmount, pmm.pmmMakerAmount, extraInfo
    );
}
```

For same-token exact-in fills, the router's actual input size is the caller-provided `exactAmount`, and the PMM calldata is later overwritten with that current fill amount:

```solidity
// contracts/BebopRouter.sol:403-408
if (exactAmount > 0) {
    calc.newFromAmount = uint256(exactAmount);
    calc.newToAmount = (order.toAmount * calc.newFromAmount) / order.fromAmount;
    calc.feeAmount = (calc.newToAmount * fee) / UNIT_BASE;
    calc.slippageAmount = (calc.newToAmount * slippage) / UNIT_BASE;
    calc.toAmountAfterFeeSlippage = calc.newToAmount - calc.feeAmount - calc.slippageAmount;
```

```solidity
// contracts/base/BebopPmmHelper.sol:207-210
bytes memory pmmCalldata = bebopPmmCalldata;
uint256 offset = selector == SWAP_SINGLE_SELECTOR ? SWAP_SINGLE_OFFSET : SWAP_AGGREGATE_OFFSET;
_changeCalldata(pmmCalldata, offset, newFromAmount);
_ensureApproval(IERC20(fromToken), bebopPmm, newFromAmount);
```

When `exactAmount < pmm.pmmTakerAmount` on that path, an amount-sensitive oracle receives the full signed PMM quote size rather than the smaller fill that settlement executes. The documented design explicitly uses PMM amounts over router-order amounts to avoid calldata-replacement manipulation, but does not distinguish full PMM quote amounts from the scaled current fill.

**Files:**

- `contracts/BebopRouter.sol` - `BebopRouter::_validateAndPrepare`, `BebopRouter::_getFeeAndSlippage`, `BebopRouter::_calculateAmounts`
- `contracts/base/BebopPmmHelper.sol` - `BebopPmmHelper::_executePmmSwap`

**Impact:** Amount-sensitive oracles can compute a slippage rate for the full PMM quote instead of the current partial fill. For typical size-dependent curves this can overcharge partial fills, because larger notional sizes usually imply larger slippage. The reference `PoolsBasedOracle` ignores the amount arguments entirely and prices only pool drift, so the mismatch is inert for that implementation. The impact is limited to custom amount-aware oracles and partial-fill execution.

**Recommended Mitigation:** Define the oracle amount semantics explicitly. If the oracle should price the current fill, pass the fill amount where it is known, such as exact-in fills, and pass a proportionally scaled maker amount:

```solidity
// Example exact-in sizing
uint256 oracleFromAmount = uint256(exactAmount);
uint256 oracleToAmount = pmm.pmmMakerAmount * oracleFromAmount / pmm.pmmTakerAmount;
```

For exact-out, where the required input depends on the returned slippage rate, either document that the oracle receives full PMM quote amounts or use an oracle API that can price exact-out targets without requiring the router to solve that circular dependency.

**Bebop:** Acknowledged.
