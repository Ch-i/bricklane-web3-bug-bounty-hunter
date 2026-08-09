---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-28-cyfrin-yieldfi-pr19-v2-0-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-05-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-28-cyfrin-yieldfi_pr19-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-28-cyfrin-yieldfi-pr19-v2-0
title: '`isNewYToken` can be omitted in YToken contracts'
vuln_class: []
---

# `isNewYToken` can be omitted in YToken contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-28-cyfrin-yieldfi_pr19-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-28-cyfrin-yieldfi_pr19-v2.0.md)_

---

**Description:** To support the accounting of underlying assets, a new parameter `isNewYToken` was introduced in `mintYToken`. This parameter is used in the [`dYTokenL1::mintYToken`](https://github.com/YieldFiLabs/contracts/blob/702a931df3adb2f6e48807203cdc7a92604ea249/contracts/core/tokens/dYTokenL1.sol#L67-L81) and [`dYTokenL2::mintYToken`](https://github.com/YieldFiLabs/contracts/blob/702a931df3adb2f6e48807203cdc7a92604ea249/contracts/core/tokens/dYTokenL2.sol#L65-L79) contracts to determine whether minting `dYTokens` should also update the balances of the underlying `YTokens`.

However, the parameter is unused in the [`YToken`](https://github.com/YieldFiLabs/contracts/blob/702a931df3adb2f6e48807203cdc7a92604ea249/contracts/core/tokens/YToken.sol#L215-L225) and [`YTokenL2`](https://github.com/YieldFiLabs/contracts/blob/702a931df3adb2f6e48807203cdc7a92604ea249/contracts/core/tokens/YTokenL2.sol#L198-L208) implementations:

```solidity
function mintYToken(address to, uint256 shares, bool isNewYToken) external virtual {
    require(msg.sender == manager, "!manager");
    _mint(to, shares);
}
```

Consider omitting the parameter to make its unused status explicit:

```diff
- function mintYToken(address to, uint256 shares, bool isNewYToken) external virtual {
+ function mintYToken(address to, uint256 shares, bool ) external virtual {
```

**YieldFi:** Fixed in commit [`a3a9bad`](https://github.com/YieldFiLabs/contracts/commit/a3a9badf7a2ef877e128add79f52453a5cbc0fa5)

**Cyfrin:** Verified. `isNewYToken` is now removed from the above function parameter declarations.
