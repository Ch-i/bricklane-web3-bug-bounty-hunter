---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Vaults can be made erroneously liquidatable due to incorrect swap path
vuln_class: []
---

# Vaults can be made erroneously liquidatable due to incorrect swap path

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** When auto redemption is executed, the `Quoter::quoteExactOutput` and `Quoter::quoteExactInput` functions of the [Uniswap v3 view-only quoter](https://github.com/Uniswap/view-quoter-v3/tree/master) are invoked for legacy and non-legacy vaults respectively. Given that these calls do not revert, execution will proceed to performing the swap; however, the swap path of `collateral -> USDC` is incorrect when attempting to swap to `USDs`:

```solidity
_amountOut = ISwapRouter(_swapRouterAddress).exactInput(
    ISwapRouter.ExactInputParams({
        path: _swapPath,
        recipient: address(this),
        deadline: block.timestamp,
        amountIn: _collateralAmount,
        // minimum amount out should be at least usd value of collateral being swapped in
        amountOutMinimum: calculator.tokenToUSD(
            ITokenManager(ISmartVaultManager(manager).tokenManager()).getTokenIfExists(_collateralAddr),
            _collateralAmount
        )
    })
);
```

The swap will succeed, converting the collateral to `USDC`, but no debt will be redeemed as the `USDs` balance of the vault has not changed:

```solidity
uint256 _usdsBalance = USDs.balanceOf(address(this));
minted -= _usdsBalance;
USDs.burn(address(this), _usdsBalance);
```

Given that `USDC` is not a valid collateral token, this will result in the vault becoming liquidatable if a sufficient amount of the collatetal token is swapped.

**Impact:** Vaults can become erroneously liquidatable as a result of auto redemption.

**Recommended Mitigation:** Ensure that the swap path is correct when performing auto redemption and add a check to ensure that the vault collateralization has not significantly decreased as a result of auto redemption.

**The Standard DAO:** Fixed by commits [3c5e136](https://github.com/the-standard/smart-vault/commit/3c5e136cdab97d88e7aa79c23ee18e50d46d6276), [821bb26](https://github.com/the-standard/smart-vault/commit/132a0138e3e586493dcd25bfb1b56e1c761f95c2#diff-821bb262cfd79a7edc00f920efc390d9572957844594bc42733fc6e70f749e9a), and [132a013](https://github.com/the-standard/smart-vault/commit/132a0138e3e586493dcd25bfb1b56e1c761f95c2). Since we are storing both input and output swap paths, we use that to more efficiently calculate the required amount to swap.

**Cyfrin:** Verified. With the introduction of the `SwapPath` struct containing both input and output paths along with the relevant swap path and target amount variables renamed to correctly reference `USDs` instead of `USDC`, this now appears to be correct so long as paths are configured as communicated (e.g. input: `WETH -> USDC -> USDs`, output: `USDs -> USDC -> WETH`).
