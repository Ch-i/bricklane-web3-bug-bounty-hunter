---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Dust amounts of swapped collateral tokens remain in `SmartVaultYieldManager`
vuln_class: []
---

# Dust amounts of swapped collateral tokens remain in `SmartVaultYieldManager`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** Due to rounding, swaps made via Uniswap-style routers with exact input parameters can result in residual dust amounts left in the calling contract. This is not an issue for deposits to Gamma Vaults, as all swapped tokens are sent to the corresponding Hypervisor contract; however, the use of [`SmartVaultYieldManager::_swapToSingleAsset`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L113-L131) called from [`SmartVaultYieldManager::_withdrawUSDsDeposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L196-L200) and [`SmartVaultYieldManager::_withdrawOtherDeposit`](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L202-L207) during withdrawals can leave dust amounts of the input token.

**Impact:** Dust amounts of collateral tokens can accumulate in `SmartVaultYieldManager` and will be utilized by the next caller for a given token.

**Recommended Mitigation:** Consider checking for non-zero residual amounts of the input token(s) to swaps made during the withdrawal of yield positions and, if present, return them to the Smart Vault.

**The Standard DAO:** Fixed by commit [`a62973e`](https://github.com/the-standard/smart-vault/commit/a62973ef32942bc74c364d20f03f03229fe8c3bb).

**Cyfrin:** Verified, dust amounts of the unwanted token are now transferred back to the sender.
