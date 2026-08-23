---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-18-cyfrin-the-standard-auto-redemption-v2-0-3-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-18-cyfrin-the-standard-auto-redemption-v2-0
title: Unused function argument in `SmartVaultYieldManager::quickDeposit` should be
  removed
vuln_class: []
---

# Unused function argument in `SmartVaultYieldManager::quickDeposit` should be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-18-cyfrin-the-standard-auto-redemption-v2.0.md)_

---

**Description:** The `SmartVaultYieldManager::quickDeposit` function has the following signature:

```solidity
function quickDeposit(address _hypervisor, address _collateralToken, uint256 _deposit)
```

However, the `_hypervisor` argument is never used and so can be removed.

**The Standard DAO:** Fixed by commit [6f943c5](https://github.com/the-standard/smart-vault/commit/6f943c51756cd8023f45af0dee403212fdab096b).

**Cyfrin:** Verified. The unused address has been removed.
