---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Insufficient deadline protection when adding/removing collateral from yield
  positions
vuln_class: []
---

# Insufficient deadline protection when adding/removing collateral from yield positions

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** When the owner of a Smart Vault transfers its collateral assets to/from one of the supported Gamma Vaults, several swaps are executed with a deadline of `block.timestamp + 60`. For example, in `SmartVaultYieldManager::_sellUSDC`:

```solidity
ISwapRouter(uniswapRouter).exactInput(ISwapRouter.ExactInputParams({
    path: _pathFromUSDC,
    recipient: address(this),
    deadline: block.timestamp + 60,
    amountIn: _balance,
    amountOutMinimum: 0
}));
```

This deadline will always be valid whenever the transaction is included in a block, with the addition of 60 seconds from the current timestamp doing nothing, as the timestamp of execution will always be `block.timestamp`.

**Impact:** The lack of a proper deadline can result in swaps being executed in market conditions that differ significantly from those intended, possibly resulting in less favorable outcomes. This is somewhat mitigated by the  `significantCollateralDrop()` protection in `SmartVaultV4`; however, this relies on Chainlink oracle values for calculation of the Smart Vault collateral that might have also changed since the transaction was submitted.

**Recommended Mitigation:** Consider allowing the user to specify a deadline for the swaps executed when adding/removing collateral from yield positions. Note that the deadline does not need to be passed directly to all swap invocations but can be checked once directly in the function bodies of `SmartVaultV4::depositYield` and `SmartVaultV4::withdrawYield`.

**The Standard DAO:** Fixed by commit [`71bad0a`](https://github.com/the-standard/smart-vault/commit/71bad0a8cc4bf8ff60321e41c9acb1e7d7fe1b2c).

**Cyfrin:** Verified, `SmartVaultV4::depositYield`, `SmartVaultV4:withdrawtYield`, and `SmartVaultV4::swap` now accept a user-supplied deadline parameter.
