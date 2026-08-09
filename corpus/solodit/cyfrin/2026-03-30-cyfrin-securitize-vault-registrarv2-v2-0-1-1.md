---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-30-cyfrin-securitize-vault-registrarv2-v2-0-1-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-30-cyfrin-securitize-vault-registrarv2-v2-0
title: '`VaultRegistrar::isRegistered` reverts instead of returning `false` when vault
  belongs to a different investor'
vuln_class: []
---

# `VaultRegistrar::isRegistered` reverts instead of returning `false` when vault belongs to a different investor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-30-cyfrin-securitize-vault-registrarv2-v2.0.md)_

---

**Description:** [`VaultRegistrar::isRegistered`](https://github.com/securitize-io/bc-vault-registrar/blob/0867ad37a9f3479dc7c26d18e757fdb07d8620c5/VaultRegistrar/contracts/VaultRegistrar.sol#L111-L129) is a view function that returns `bool`. It correctly returns `false` when the vault or investor is unregistered (empty ID), but when both have non-empty IDs that don't match, it delegates to [`_validateVaultBelongsToInvestor`](https://github.com/securitize-io/bc-vault-registrar/blob/0867ad37a9f3479dc7c26d18e757fdb07d8620c5/VaultRegistrar/contracts/VaultRegistrar.sol#L170-L178), which reverts with `VaultBelongsToDifferentInvestor` instead of returning `false`.

**Impact:** Any contract calling `isRegistered` as a boolean query will revert instead of receiving `false` when the vault is registered under a different investor. This breaks composability and can DoS downstream contracts that rely on it as a safe view check.

**Recommended Mitigation:** Replace the revert path with a `false` return:

```diff
-     _validateVaultBelongsToInvestor(vaultAddress, vaultInvestorId, investorId);
+     if (keccak256(bytes(vaultInvestorId)) != keccak256(bytes(investorId))) {
+         return false;
+     }

      return true;
```

**Securitize:** Fixed in commit [6b4a9e5](https://github.com/securitize-io/bc-vault-registrar/commit/6b4a9e5185290c4cf1ab8b5bb049a9074594f984).

**Cyfrin:** Verified. `VaultRegistrar::isRegistered` now returns false when the vault belongs to a different investor.

\clearpage
