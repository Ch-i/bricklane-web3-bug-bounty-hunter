---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: '`YtokenL2::previewMint` and `YTokenL2::previewWithdraw` round in favor of
  user'
vuln_class: []
---

# `YtokenL2::previewMint` and `YTokenL2::previewWithdraw` round in favor of user

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** For the L2 `YToken` contracts, assets are not managed directly. Instead, the vault’s exchange rate is provided by an oracle, using the exchange rate from L1 as the source of truth.

This architectural choice requires custom implementations of functions like `previewMint`, `previewDeposit`, `previewRedeem`, and `previewWithdraw`, as well as the internal `_convertToShares` and `_convertToAssets`. These have been re-implemented to rely on the oracle-provided exchange rate instead of local accounting.

However, both `previewMint` and `previewWithdraw` currently perform rounding in favor of the user:

- [`YTokenL2::previewMint`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YTokenL2.sol#L249-L250):
  ```solidity
  // Calculate assets based on exchange rate
  return (grossShares * exchangeRate()) / Constants.PINT;
  ```
- [`YTokenL2::previewWithdraw`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/tokens/YTokenL2.sol#L261-L262):
  ```solidity
  // Calculate shares needed for requested assets based on exchange rate
  uint256 sharesWithoutFee = (assets * Constants.PINT) / exchangeRate();
  ```

This behavior contradicts the [security recommendations in EIP-4626](https://eips.ethereum.org/EIPS/eip-4626#security-considerations), which advise rounding in favor of the vault to prevent value leakage.

**Impact:** By rounding in favor of the user, these functions allow users to receive slightly more shares or assets than they should. While the two-step withdrawal process limits the potential for immediate exploitation, this rounding error can result in a slow and continuous value leak from the vault—especially over many transactions or in the presence of automation.

**Recommended Mitigation:** Update `previewMint` and `previewWithdraw` to round in favor of the vault. This can be done by adopting the modified `_convertToShares` and `_convertToAssets` functions with explicit rounding direction, similar to the approach used in the [OpenZeppelin ERC-4626 implementation](https://github.com/OpenZeppelin/openzeppelin-contracts-upgradeable/blob/master/contracts/token/ERC20/extensions/ERC4626Upgradeable.sol#L177-L185).

**YieldFi:** Fixed in commit [`a820743`](https://github.com/YieldFiLabs/contracts/commit/a82074332cc1f57eba398100c3a43e8a70a4c8ce)

**Cyfrin:** Verified. the preview functions now utilizes `_convertToShares` and `_convertToAssets` with the correct rounding direction.
