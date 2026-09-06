---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: '`USDC` cannot be added as an accepted collateral token'
vuln_class: []
---

# `USDC` cannot be added as an accepted collateral token

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** At least 10% of each collateral deposit to Gamma must be directed toward the `USDs/USDC` pool underlying the `USDs` Hypervisor:

```solidity
function _usdDeposit(address _collateralToken, uint256 _usdPercentage, bytes memory _pathToUSDC) private {
    _swapToUSDC(_collateralToken, _usdPercentage, _pathToUSDC);
    _swapToRatio(USDC, usdsHypervisor, ramsesRouter, 500);
    _deposit(usdsHypervisor);
}
```

During this process, [`SmartVaultYieldManager::_swapToUSDC`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L133-L144) swaps the collateral token to `USDC`; however, this would fail for `USDC` without additional handling as it has no path to itself. A similar issue is present in [`SmartVaultYieldManager::_sellUSDC`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L182-L194) when attempting to withdraw the `USDs` Hypervisor deposits to USDC.

Additionally, assuming the was correctly handled, broad use of [`SmartVaultYieldManager::thisBalanceOf`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L49-L51) would result in the entire balance of USDC being utilized for the `USDs` Hypervisor deposit within [`SmartVaultYieldManager::_swapToRatio`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L60-L61) without considering the subsequent Hypervisor deposit:

```solidity
uint256 _tokenBBalance = _thisBalanceOf(_tokenB);
(uint256 _amountStart, uint256 _amountEnd) = IUniProxy(uniProxy).getDepositAmount(_hypervisor, _tokenA, _thisBalanceOf(_tokenA));
```

Furthermore, if `USDC` were to be added as an accepted collateral token, this would result in liquidations being blocked for blacklisted Smart Vaults. An attacker could deposit illegally-obtained `USDC` into their Smart Vault, borrowing `USDs` and avoiding ever being liquidated as the attempt by the protocol to transfer these tokens out would fail.

**Impact:** `USDC` cannot be added as an accepted collateral.

**Recommended Mitigation:** These issues should first be addressed if it is desired to add `USDC` as an accepted collateral token.

**The Standard DAO:** Acknowledged. Not fixing because we have no intentions to add `USDC` as a collateral type. If we were to add it, we believe it would still be fine, as long we didn’t add hypervisor data for it. This seems acceptable to us.

**Cyfrin:** Acknowledged.
