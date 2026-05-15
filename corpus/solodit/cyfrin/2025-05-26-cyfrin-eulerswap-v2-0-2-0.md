---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-26-cyfrin-eulerswap-v2-0-2-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-05-26T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-26-cyfrin-eulerswap-v2-0
title: Unnecessary extra storage reads when swapping
vuln_class: []
---

# Unnecessary extra storage reads when swapping

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-26-cyfrin-eulerswap-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-26-cyfrin-eulerswap-v2.0.md)_

---

**Description:** When a swap is executed, whether via EulerSwap or Uniswap V4, a reentrant hook is employed:

[`UniswapHook::nonReentrantHook`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/UniswapHook.sol#L67-L80):

```solidity
modifier nonReentrantHook() {
    {
        CtxLib.Storage storage s = CtxLib.getStorage();
        require(s.status == 1, LockedHook());
        s.status = 2;
    }

    _;

    {
        CtxLib.Storage storage s = CtxLib.getStorage();
        s.status = 1;
    }
}
```

Here, `CtxLib.getStorage()` is called once to load the storage struct and set `status` to `2`, then again afterward to restore `status` back to `1`.

Later in the swap flow, the same storage slot is reloaded multiple times:

1. In [`QuoteLib::calcLimits`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/libraries/QuoteLib.sol#L70-L71):

   ```solidity
   function calcLimits(IEulerSwap.Params memory p, bool asset0IsInput) internal view returns (uint256, uint256) {
       CtxLib.Storage storage s = CtxLib.getStorage();
       …
   }
   ```
2. In [`QuoteLib::findCurvePoint`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/libraries/QuoteLib.sol#L150-L155):

   ```solidity
   function findCurvePoint(IEulerSwap.Params memory p, uint256 amount, bool exactIn, bool asset0IsInput)
       internal
       view
       returns (uint256 output)
   {
       CtxLib.Storage storage s = CtxLib.getStorage();
       …
   }
   ```
3. And again in [`UniswapHook::_beforeSwap`](https://github.com/euler-xyz/euler-swap/blob/1022c0bb3c034d905005f4c5aee0932a66adf4f8/src/UniswapHook.sol#L129) just before updating reserves:

   ```solidity
   CtxLib.Storage storage s = CtxLib.getStorage();
   ```

Each `getStorage()` call emits an extra SLOAD, increasing the overall gas cost of the swap.


Consider embedding the non-reentrant logic directly within `_beforeSwap`, fetch storage only once, and cache the reserve values for use in the CurveLib calls. For example:

```solidity
function _beforeSwap(
    address,
    PoolKey calldata key,
    IPoolManager.SwapParams calldata params,
    bytes calldata
)
    internal
    override
    returns (bytes4, BeforeSwapDelta, uint24)
{
    IEulerSwap.Params memory p = CtxLib.getParams();

    // Single storage load and reentrancy guard
    CtxLib.Storage storage s = CtxLib.getStorage();
    require(s.status == 1, LockedHook());
    s.status = 2;

    // Cache reserves locally
    uint112 reserve0 = s.reserve0;
    uint112 reserve1 = s.reserve1;

    // … perform limit and curve-point calculations using reserve0/reserve1 …

    // Update reserves and release guard
    s.reserve0 = uint112(newReserve0);
    s.reserve1 = uint112(newReserve1);
    s.status = 1;

    return (BaseHook.beforeSwap.selector, returnDelta, 0);
}
```

By doing so, you eliminate redundant storage reads, reducing gas consumption on every swap. Same goes for the `EulerSwap::swap` flow as well.


**Euler:** Acknowledged.
