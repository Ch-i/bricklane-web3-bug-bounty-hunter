---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: 5. Create a registrar
vuln_class: []
---

# 5. Create a registrar

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

One registrar serves one mint. Several registrars may exist for the same mint; each gets its
own id and its own PDAs.
```
However, `thaw_vault_token_account_spl` only verifies that:
- the caller is the admin of the supplied registrar;
- the mint matches that registrar;
- the vault has a valid global InvestorRegistry.
and few more checks but registrar does not prove that the vault belongs to that specific registrar. Registrar A's admin can pass B's vaults to `thaw_vault_token_account_spl` and A can remove the frozen state from B’s vault, potentially allowing it to receive or transfer tokens despite B’s intended compliance or administrative freeze.

**Impact:** Registrar A’s admin can:
1. Use Registrar A’s state and authority PDA.
2. Pass Registrar B’s vault wallet and token account.
3. Pass the canonical registry for (mint, B’s vault).
4. Cause Registrar A’s authority to thaw B’s frozen vault.
This can reverse a freeze imposed on B’s vault and allow it to receive or transfer tokens. It also causes the emitted thaw event to attribute the action to Registrar A, even though the vault may have been registered through Registrar B. This broadens the admin's effective freeze authority beyond the documented vault-repair use case.

**Recommended Mitigation:** Bind every vault to the registrar that registered it.

**Securitize:** Fixed in commit [de22499](https://github.com/securitize-io/bc-solana-whitelister/commit/de224992a7e3ce5849c91f583ad1f9c698ece63f).

**Cyfrin:** Verified.

\clearpage
