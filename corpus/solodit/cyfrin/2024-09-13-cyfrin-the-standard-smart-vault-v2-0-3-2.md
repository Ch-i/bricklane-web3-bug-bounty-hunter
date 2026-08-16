---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-3-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Inconsistent use of equivalent function parameter and immutable variable in
  `SmartVaultYieldManager::_withdrawUSDsDeposit` is confusing
vuln_class: []
---

# Inconsistent use of equivalent function parameter and immutable variable in `SmartVaultYieldManager::_withdrawUSDsDeposit` is confusing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When withdrawing collateral from the `USDs` Hypervisor in `SmartVaultYieldManager::_withdrawUSDsDeposit`, the `_hypervisor` parameter will always be equal to the immutable `usdsHypervisor` variable due to the following [conditional check](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L211-L213) in `SmartVaultYieldManager::withdraw`:

```solidity
_hypervisor == usdsHypervisor ?
    _withdrawUSDsDeposit(_hypervisor, _token) :
    _withdrawOtherDeposit(_hypervisor, _token);
```

However, a mixture of both the `_hypervisor` parameter and the equivalent immutable variable is used within[`SmartVaultYieldManager::_withdrawUSDsDeposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L196-L200):

```solidity
    function _withdrawUSDsDeposit(address _hypervisor, address _token) private {
    IHypervisor(_hypervisor).withdraw(_thisBalanceOf(_hypervisor), address(this), address(this), [uint256(0),uint256(0),uint256(0),uint256(0)]);
    _swapToSingleAsset(usdsHypervisor, USDC, ramsesRouter, 500);
    _sellUSDC(_token);
}
```

This is confusing to the reader as it could imply that the `_hypervisor` parameter differs from the immutable `usdsHypervisor`, which is not the case.

**Recommended Mitigation:** Consider consistent utilization of either the `_hypervisor` parameter or the immutable `usdsHypervisor` variable.

**The Standard DAO:** Fixed by commit [`f601a11`](https://github.com/the-standard/smart-vault/commit/f601a1173e0b2e2006e73c13339051ae7c7e6af1).

**Cyfrin:** Verified, the immutable variable is now used exclusively.
