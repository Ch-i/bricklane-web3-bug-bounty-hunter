---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-4-2
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[I-03] Unsafe to close stake_account_info_pda'
vuln_class: []
---

# [I-03] Unsafe to close stake_account_info_pda

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Original severity:** Best Practices

**Files:** [`update.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/dba32c9fce1310b23f9d1a5a0407602bcd7446b7/programs/liquid-unstaker/src/instructions/update.rs#L156)

**Description:**

In the `update(...)` instruction, lamports are withdrawn from the `stake_account`, and the related `stake_account_info_pda` account is closed.

```rust
for stake_account_info_pda in stake_account_info_pda_remaining_accounts {

    total_rent_amount += stake_account_info_pda.get_lamports();
    **stake_account_info_pda.try_borrow_mut_lamports()? = 0;
}
```

However, the method for closing `stake_account_info_pda` is to transfer out all lamports, and the data clearing occurs after the transaction ends. A malicious caller of the `update(...)` instruction could provide lamports to `stake_account_info_pda` before the transaction ends, preventing the account from being closed.

**Impact:** If the closed `stake_account` is re-initialized as a `stake_account`, it cannot interact with the vault because the `stake_account_info_pda` was not closed.

**Recommendation:** It is recommended to deterministically set the `stake_account_info_pda` space to 0.

**Status:** Fixed

**Update from The Vault:** [472730d353adca49fab795f1c5c20c3c42bcada5](https://github.com/SolanaVault/liquid-unstaker/commit/472730d353adca49fab795f1c5c20c3c42bcada5).
