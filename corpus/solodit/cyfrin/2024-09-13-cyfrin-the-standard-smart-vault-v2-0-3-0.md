---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-3-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Unnecessary typecast of `msg.sender` to `address`
vuln_class: []
---

# Unnecessary typecast of `msg.sender` to `address`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** There is an [instance](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultYieldManager.sol#L169) of the `msg.sender` context variable that is unnecessarily cast to `address` in `SmartVaultYieldManager::deposit`:

```solidity
uint256 _balance = IERC20(_collateralToken).balanceOf(address(msg.sender));
```

**Recommended Mitigation:** Consider removing the `address` typecast as `msg.sender` is already an address.

**The Standard DAO:** Fixed by commit [`1a9dc5f`](https://github.com/the-standard/smart-vault/commit/1a9dc5fc3f553d1b3dbf285e863d0f8cf5f8bbc0).

**Cyfrin:** Verified, typecast has been removed.
