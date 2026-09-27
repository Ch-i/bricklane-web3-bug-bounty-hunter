---
affected_contracts: []
derives_from: []
id: solodit-codespect-2026-02-04-dutch-protocol-0-5
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-02-04T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md
tags:
- firm:codespect
- report:2026-02-04-dutch-protocol
title: '[H-06] Tax fee revenue may be lost due to Uniswap V4 trading'
vuln_class: []
---

# [H-06] Tax fee revenue may be lost due to Uniswap V4 trading

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2026-02-04-Dutch-Protocol.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2026-02-04-Dutch-Protocol.md)_

---

**Files:** [`DUTCHBondingHook.sol`](https://github.com/dutch-protocol/Protocol-Contracts/tree/cec8b243aa645fdbe80e05e613eca69542b62a2e/src/DUTCHBondingHook.sol#L985)

**Description:**

By design, mainstream DEXs are expected to be blacklisted for DUTCH tokens to restrict off-market trading, ensuring that all trades go through the `DUTCHBondingHook` and incur a tax fee. The `DUTCHBondingHook` overrides `_beforeSwap(...)` so that when a user trades via Uniswap V4 swap, the calculation does not go through the AMM but is performed using a custom curve.

```solidity
function _executeBuy(...) internal returns (...) {
    //...
    // Take WETH from pool (user already deposited it).
    poolManager.take(_wethCurrency, address(this), inputAmount_);

    // Distribute tax.
    (uint256 vaultAmount_, uint256 opsAmount_) =
        _calculateBuyTax(taxAmount_);
    IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
        _dutchVault,
        vaultAmount_
    );
    IERC20(Currency.unwrap(_wethCurrency)).safeTransfer(
        _opsWallet,
        opsAmount_
    );

    // Mint DUTCH to hook.
    dutchToken.mint(address(this), outputAmount_);
    //...
}
```

During the purchase process, `DUTCHBondingHook` calls `take(...)` to withdraw WETH from the pool, mints DUTCH to send to the pool, and calls `settle(...)` to update the account. The Hook `accountDelta` are transferred to the sender in `afterSwap`. Afterwards, the sender must repay the WETH to the Hook and withdraw DUTCH from the pool. The above process prevents the Uniswap V4 `PoolManager` from being blacklisted for DUTCH tokens, because this contract must handle sending tokens to the buyer during the purchase process.

**Impact:** This allows off-market trading to occur on Uniswap V4. Users can create DUTCH-related pools and trade without using the `DUTCHBondingHook`, causing the protocol to lose tax fee revenue.

**Recommendation:** It is recommended to send DUTCH directly to the user during the purchase process, instead of involving the `PoolManager` in the DUTCH token transfer. This way, the `PoolManager` can be blacklisted to prevent off-market trading on Uniswap V4.

**Status:** Fixed

**Client response:** Fixed in [9da861422e64236acfe61feb3efcc0ccbbe5f49a](https://github.com/dutch-protocol/Protocol-Contracts/commit/9da861422e64236acfe61feb3efcc0ccbbe5f49a)

**CODESPECT fix review:** Fixed. Since the Hook design was removed, Uniswap V4 can be added to the blacklist.
