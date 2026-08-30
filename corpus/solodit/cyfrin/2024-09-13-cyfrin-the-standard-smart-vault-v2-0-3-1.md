---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Comment incorrectly refers to `€` when it should be `$`
vuln_class: []
---

# Comment incorrectly refers to `€` when it should be `$`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** The following comment is [present](https://github.com/the-standard/smart-vault/blob/c6837d4a296fe8a6e4bb5e0280a66d6eb8a40361/contracts/SmartVaultV4.sol#L91) when summing the stablecoin collateral in `SmartVaultV4::yieldVaultCollateral`:

```solidity
// both USDs and its vault pair are € stablecoins, but can be equivalent to €1 in collateral
```

Here, the `€` symbol is used for USD instead of `$`.

**Recommended Mitigation:** Update the comment to use the `$` symbol.

**The Standard DAO:** No longer applicable. Comment removed in commit [`5862d8e`](https://github.com/the-standard/smart-vault/commit/5862d8e10ac8648b89a7e3a78498ff20dc31e42e).

**Cyfrin:** Verified, comment has been removed.
