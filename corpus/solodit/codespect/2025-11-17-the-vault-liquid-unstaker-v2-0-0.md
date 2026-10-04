---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[C-01] The flash_borrow(...) instruction can be used to drain the vault'
vuln_class: []
---

# [C-01] The flash_borrow(...) instruction can be used to drain the vault

_Section severity (from Solodit section header): Critical_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`state.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/dba32c9fce1310b23f9d1a5a0407602bcd7446b7/programs/liquid-unstaker/src/state.rs#L104)

**Description:**

The `flash_borrow(...)` instruction allows users to perform flash loans using funds from the vault. The user is required to include a `flash_repay(...)` instruction later in the same transaction to repay the loan. During the flash loan, the borrowed amount is recorded in `flash_loan_borrowed_amount`, and `sol_vault_lamports` decreases accordingly. However, when calculating the vault’s share price, only `sol_vault_lamports` is considered, while `flash_loan_borrowed_amount` is ignored. This causes the share value to drop temporarily during the flash loan.

```rust
pub fn flash_borrow(&mut self, amount: u64) -> Result<()> {
    self.flash_loan_borrowed_amount = amount;
    self.sol_vault_lamports = self.sol_vault_lamports
        .checked_sub(amount)
        .ok_or(error!(crate::error::LiquidUnstakerErrorCode::InsufficientSolVaultBalance))?;
    Ok(())
}
```

**Impact:** An attacker can exploit this mechanism to drain the vault by performing an arbitrage: they first initiate a flash loan to reduce the share value, and then mint shares at the temporarily low price. After repaying the flash loan, `sol_vault_lamports` returns to normal, causing the share value to rise again. Then the attacker can burn their shares for profit.

**Recommendation:** It is recommended to prohibit interactions with the vault during the flash loan process.

**Status:** Fixed

**Update from The Vault:** Resolved in [140cc52e5bc519fc9a1c223987c8d8f5d0c001ac](https://github.com/SolanaVault/liquid-unstaker/commit/140cc52e5bc519fc9a1c223987c8d8f5d0c001ac) and [9aeeaa21ee6efed2524d0f32dbef306c103697f2](https://github.com/SolanaVault/liquid-unstaker/commit/9aeeaa21ee6efed2524d0f32dbef306c103697f2).
