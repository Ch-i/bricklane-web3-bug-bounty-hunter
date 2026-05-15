---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Unused return value can be removed
vuln_class: []
---

# Unused return value can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The `IRedeemableLegacy::autoRedemption` function signature is as follows:

```solidity
function autoRedemption(
    address _swapRouterAddress,
    address _collateralAddr,
    bytes memory _swapPath,
    uint256 _amountIn
) external returns (uint256 _redeemed);
```

Within `SmartVaultV4Legact::autoRedemption`, the `_amountOut` return value is bubbled-up by `SmartVaultManagerV6::vaultAutoRedemption`:

```solidity
function vaultAutoRedemption(
    address _smartVault,
    address _collateralAddr,
    bytes memory _swapPath,
    uint256 _collateralAmount
) external onlyAutoRedemption returns (uint256 _amountOut) {
    return IRedeemableLegacy(_smartVault).autoRedemption(swapRouter, _collateralAddr, _swapPath, _collateralAmount);
}
```

However, it is never actually removed and so can be removed from both function signatures.

```solidity
function legacyAutoRedemption(
    address _smartVault,
    address _token,
    bytes memory _collateralToUSDCPath,
    uint256 _USDsTargetAmount,
    uint256 _estimatedCollateralValueUSD
) private {
    ...
    ISmartVaultManager(smartVaultManager).vaultAutoRedemption(_smartVault, _token, _collateralToUSDCPath, _amountIn);
}
```

**The Standard DAO:** Fixed by commit [2c58fa5](https://github.com/the-standard/smart-vault/commit/2c58fa5759b2d31162f31fdca7c0227a1ef08302).

**Cyfrin:** Verified. The return value is now used to emit an event.
