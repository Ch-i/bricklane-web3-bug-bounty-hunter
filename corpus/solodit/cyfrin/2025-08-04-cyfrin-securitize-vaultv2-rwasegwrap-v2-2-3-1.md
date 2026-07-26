---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md
tags:
- firm:cyfrin
- report:2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2-2
title: Unnecessary gas consumption in deposit function due to redundant maximum deposit
  check
vuln_class: []
---

# Unnecessary gas consumption in deposit function due to redundant maximum deposit check

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-04-cyfrin-securitize-vaultv2-rwasegwrap-v2.2.md)_

---

**Description:** The `SecuritizeVaultV2::_depositWithFee` function performs an unnecessary check against `maxDeposit(from)` to validate that the deposit amount doesn't exceed the maximum allowed deposit limit. However, `SecuritizeVaultV2` does not override the `maxDeposit` function from its parent `ERC4626Upgradeable` contract, which means `maxDeposit` always returns `type(uint256).max`.

```solidity
// In SecuritizeVaultV2::_depositWithFee
function _depositWithFee(uint256 assets, address from) private returns (uint256) {
    address caller = _msgSender();
    uint256 maxAssets = maxDeposit(from); // Returns type(uint256).max
    if (assets > maxAssets) { // This condition will never be true
        revert ERC4626ExceededMaxDeposit(from, assets, maxAssets);
    }
    // ... rest of function
}

// In ERC4626Upgradeable (not overridden by SecuritizeVaultV2)
function maxDeposit(address) public view virtual returns (uint256) {
    return type(uint256).max; // Always returns maximum uint256 value
}
```
This creates a redundant comparison where `assets > type(uint256).max` will never be true for any realistic deposit amount, making the check pointless and wasteful of gas. The condition on line 346-348 will never trigger the revert `ERC4626ExceededMaxDeposit` because no uint256 value can exceed `type(uint256).max`.

The function call `maxDeposit(from)` and the subsequent comparison are executed on every deposit operation, unnecessarily consuming gas for a check that serves no purpose in the current implementation.

**Impact:** This unnecessary computation increases gas costs for every deposit operation without providing any functional benefit, resulting in higher transaction costs for users.

**Recommended Mitigation:** Remove the unnecessary maximum deposit check since `SecuritizeVaultV2` doesn't implement custom deposit limits:

```diff
function _depositWithFee(uint256 assets, address from) private returns (uint256) {
    address caller = _msgSender();
-   uint256 maxAssets = maxDeposit(from);
-   if (assets > maxAssets) {
-       revert ERC4626ExceededMaxDeposit(from, assets, maxAssets);
-   }

    uint256 fee = 0;
    if (address(feeManager) != address(0)) {
        fee = IFeeManager(feeManager).computeFee(IFeeManager.FeeApplicableOperation.Deposit, assets);
    }

    uint256 shares = previewDeposit(assets - fee);
    _depositAndSendFees(caller, from, assets, fee, shares);
    return shares;
}
```

Alternatively, if deposit limits are intended to be implemented in the future, override the `maxDeposit` function with the appropriate logic.

**Securitize:** Fixed in commits [5105f0](https://github.com/securitize-io/bc-securitize-vault-sc/commit/5105f03e95502fc887241e47f660996e9163d3e8) and [57805a](https://github.com/securitize-io/bc-rwa-seg-wrap-sc/commit/57805a83958e87e3f9b3677caf8554c09bd8fad0).

**Cyfrin:** Verified.
