---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Incorrect collateral quote amounts due to use of incorrect swap path
vuln_class: []
---

# Incorrect collateral quote amounts due to use of incorrect swap path

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** Within `AutoRedemption::legacyAutoRedemption`, the amount of input collateral required is calculated as:

```solidity
(uint256 _approxAmountInRequired,,,) =
IQuoter(quoter).quoteExactOutput(_collateralToUSDCPath, _USDsTargetAmount);
uint256 _amountIn = _approxAmountInRequired > _collateralBalance ? _collateralBalance : _approxAmountInRequired;
```

This quote is incorrect as it uses the `collateral -> USDC` swap path for calculation of a target `USDs` amount. Since `USDs` is expected to be below peg for this logic to be triggered, it will take more collateral to swap to `_USDsTargetAmount` amount of `USDC` compared to that of `USDs`. Furthermore, `Quoter::quoteExactOutput` expects the path to be reversed when calculating the amount of the input token required to be swapped for an exact amount of the output token.

Similarly, in `SmartVaultV4::calculateAmountIn`, the swap path is `collateral -> USDC` but the amount output is compared to a `USDs` target amount (which is incorrectly named as `_USDCTargetAmount`):

```solidity
(uint256 _quoteAmountOut,,,) = IQuoter(_quoterAddress).quoteExactInput(_swapPath, _collateralBalance);
return _quoteAmountOut > _USDCTargetAmount
    ? _collateralBalance * _USDCTargetAmount / _quoteAmountOut
    : _collateralBalance;
```

**Impact:** The `_amountIn` variable will be inflated, causing more collateral to be swapped to `USDs` than needed to restore peg.

**Recommended Mitigation:** Use the reversed `collateral -> USDs` swap path to calculate the required amount in.

**The Standard DAO:** Fixed by commit [3c5e136](https://github.com/the-standard/smart-vault/commit/3c5e136cdab97d88e7aa79c23ee18e50d46d6276).

**Cyfrin:** Verified. With the introduction of the `SwapPath` struct containing both input and output paths along with the relevant swap path and target amount variables renamed to correctly reference `USDs` instead of `USDC`, this now appears to be correct so long as paths are configured as communicated (e.g. input: `WETH -> USDC -> USDs`, output: `USDs -> USDC -> WETH`.
