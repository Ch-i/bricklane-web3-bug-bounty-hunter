---
affected_contracts: []
derives_from: []
id: solodit-hexens-2025-02-03-rush-trading-1-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-02-03T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md
tags:
- firm:hexens
- report:2025-02-03-rush-trading
title: '[RUSH1-4] Lack of slippage protection in withdraw functions'
vuln_class: []
---

# [RUSH1-4] Lack of slippage protection in withdraw functions

_Section severity (from Solodit section header): Medium_  
_Audit firm: Hexens_  
_Source report: [2025-02-03-Rush-Trading.md](https://github.com/solodit/solodit_content/blob/main/reports/Hexens/2025-02-03-Rush-Trading.md)_

---

**Severity:** Medium

**Path:** src/periphery/RushRouter.sol, src/periphery/RushRouterAlpha.sol

**Description:** The `withdraw()` and `withdrawETH()` functions both call `redeem()` on the LiquidityPool. However, these functions don't have a slippage protection feature, meaning the depositor may not use the exact number of shares they expect. The value of shares used is based on the total token balance in the LiquidityPool, which can change, especially if new funds are added. This fluctuation can lead to using more shares than anticipated when withdrawing.
```
   function withdraw(uint256 amount) external {
        // Calculate the amount of shares to redeem.
        uint256 shares = LIQUIDITY_POOL.previewWithdraw(amount);

        // Transfer the amount of shares to this contract.
        IERC20(LIQUIDITY_POOL).transferFrom({ from: msg.sender, to: address(this), value: shares });

        // Redeem the amount of shares from the LiquidityPool and transfer the corresponding amount of WETH to the
        // sender.
        LIQUIDITY_POOL.redeem({ shares: shares, receiver: msg.sender, owner: address(this) });
    }

    /**
     * @notice Withdraw lent ETH from the LiquidityPool.
     * @param amount The amount of ETH to withdraw.
     */
    function withdrawETH(uint256 amount) external {
        // Calculate the amount of shares to redeem.
        uint256 shares = LIQUIDITY_POOL.previewWithdraw(amount);

        // Transfer the amount of shares to this contract.
        IERC20(LIQUIDITY_POOL).transferFrom({ from: msg.sender, to: address(this), value: shares });

        // Redeem the amount of shares from the LiquidityPool and transfer the corresponding amount of WETH to this
        // contract.
        uint256 received = LIQUIDITY_POOL.redeem({ shares: shares, receiver: address(this), owner: address(this) });

        // Withdraw the received WETH to ETH.
        IWETH(WETH).withdraw(received);

        // Transfer the amount of WETH to the sender.
        payable(msg.sender).transfer(received);
    }
```


**Remediation:**  Allow users to specify a maximum number of shares to use when withdrawing from `LiquidityPool`.

**Status:**  Fixed


- - -
