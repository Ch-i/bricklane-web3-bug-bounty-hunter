---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Hardcoded pool fees can result in increased slippage and failed swaps
vuln_class: []
---

# Hardcoded pool fees can result in increased slippage and failed swaps

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** The issue raised in the previous CodeHawks contest as report item [M-03](https://codehawks.the-standard.io/c/2023-12-the-standard/s/483) remains present in `SmartVaultV4::swap` where the pool fee is [hardcoded](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L267) to `3000`:

```solidity
ISwapRouter.ExactInputSingleParams memory params = ISwapRouter.ExactInputSingleParams({
        tokenIn: inToken,
        tokenOut: getTokenisedAddr(_outToken),
        fee: 3000, // @audit hardcoded pool fee
        recipient: address(this),
        deadline: block.timestamp + 60,
        amountIn: _amount - swapFee,
        amountOutMinimum: minimumAmountOut,
        sqrtPriceLimitX96: 0
    });
```

The same issue is present within [`SmartVaultYieldManager::_usdDeposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L158) and [`SmartVaultYieldManager::_withdrawDeposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L198), where collateral tokens are swapped to/from `USDC` and `USDs` with a hardcoded pool fee of `500`:

```solidity
function _usdDeposit(address _collateralToken, uint256 _usdPercentage, bytes memory _pathToUSDC) private {
    _swapToUSDC(_collateralToken, _usdPercentage, _pathToUSDC);
    _swapToRatio(USDC, usdsHypervisor, ramsesRouter, 500);
    _deposit(usdsHypervisor);
}
...
function _withdrawUSDsDeposit(address _hypervisor, address _token) private {
    IHypervisor(_hypervisor).withdraw(_thisBalanceOf(_hypervisor), address(this), address(this), [uint256(0),uint256(0),uint256(0),uint256(0)]);
    _swapToSingleAsset(usdsHypervisor, USDC, ramsesRouter, 500);
    _sellUSDC(_token);
}
```

**Impact:** As mentioned in [M-03](https://codehawks.the-standard.io/c/2023-12-the-standard/s/483) of the CodeHawks contest, with the possible exception of the `USDs/USDC` pool created and maintained by the protocol, the pool with the highest liquidity will not necessarily always be equal to the hardcoded values, so trading in a pool with low liquidity will result in increased slippage or failed swaps. If the loss exceeds 10% of the collateral value, this results in a DoS of yield deposits/withdrawals due to validation in [`SmartVaultV4::significantCollateralDrop`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L295-L297). For calls to `SmartVaultV4::swap`, there is no such validation to prevent the Smart Vault from being put unnecessarily close to liquidation – the minimum amount output from the swap is that required to remain collateralized within 1% of liquidation.

**Recommended Mitigation:** The same recommendation as in [M-03](https://codehawks.the-standard.io/c/2023-12-the-standard/s/483) applies here – consider allowing the user to pass the pool fee as a parameter to the call(s).

**The Standard DAO:** Collateral swap pool fees fixed by commit [`f9f7093`](https://github.com/the-standard/smart-vault/commit/f9f70930168499f2de6b7aadf49995b7a766f1a1). Hypervisor swap pool fees acknowledged – not fixed as these swap routes will be managed by admins in `hypervisorData`.

**Cyfrin:** Verified, `SmartVaultV4::swap` now accepts a user-supplied pool fee parameter.
