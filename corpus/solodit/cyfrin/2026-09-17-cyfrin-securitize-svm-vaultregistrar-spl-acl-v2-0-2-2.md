---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0-2-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2-0
title: '`thaw_vault_token_account_spl` unconditionally CPIs ACL `thaw_account` and
  reverts on an already-thawed vault token account, unlike the guarded `register_vault_spl`
  path'
vuln_class: []
---

# `thaw_vault_token_account_spl` unconditionally CPIs ACL `thaw_account` and reverts on an already-thawed vault token account, unlike the guarded `register_vault_spl` path

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-17-cyfrin-securitize-svm-vaultregistrar-spl-acl-v2.0.md)_

---

**Description:** `thaw_vault_token_account_spl` invokes the ACL `thaw_account` CPI unconditionally without first checking whether the vault token account is frozen, whereas the `register_vault_spl` path guards the identical CPI with `thaw_vault_token_account_if_frozen` returning early unless `vault_token_account.state == AccountState::Frozen`. Because `vault_token_account` is declared `init_if_needed`, on a mint without a `DefaultAccountState` extension a missing vault token account is created already thawed, and the token-2022 `thaw_account` then rejects the already-thawed account, reverting the transaction.

**Impact:** The standalone thaw instruction is non-idempotent: on the default mint configuration it can never create-and-thaw a missing vault token account, breaking the administrative restore path it exists to serve. The instruction is admin-only and involves no fund loss or third-party harm, so the impact is confined to a broken admin repair flow.

**Recommended Mitigation:** Mirror the registration-path guard by reading `vault_token_account.state` and skipping the `thaw_account` CPI when it is not `AccountState::Frozen`.

**Securitize:** Fixed in commit [4d2b2b1](https://github.com/securitize-io/bc-solana-whitelister/commit/4d2b2b17ebdf798dd376f1b78f54578dee45e2a0).

**Cyfrin:** Verified.
