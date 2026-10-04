---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-2-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[M-01] The withdraw_stake_account(...)instruction may dilute vault rewards'
vuln_class: []
---

# [M-01] The withdraw_stake_account(...)instruction may dilute vault rewards

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`withdraw_stake_account.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/withdraw_stake_account.rs)

**Description:**

The `withdraw_stake_account(...)` instruction allows users to withdraw funds by splitting the `stake_account` using the `split(...)` instruction before the `stake_account` is deactivated. However, since the `stake_account` may earn staking rewards at the end of the epoch, these rewards would normally be allocated to the vault after the update instruction. Allowing the `stake_account` to be split early could cause rewards that were originally meant for the vault to be allocated to the withdrawing user instead. At the same time, when `stake_account_info_source.stake_lamports` equals 0, `stake_account_info_source` will be closed without checking whether there are still funds in the `stake_account` (e.g., donated lamports). This could result in some funds in the `stake_account` being stuck or if the amount left is smaller than `minimum_delegation_amount` the instruction will fail.

```rust
if ctx.accounts.stake_account_info_source.stake_lamports == 0 {
    // Close the PDA if all stake has been withdrawn (and remaining lamports transferred to vault)
    let before_vault_lamports = ctx.accounts.sol_vault.lamports();
    ctx.accounts.stake_account_info_source.close(ctx.accounts.sol_vault.to_account_info())?;
    let after_vault_lamports = ctx.accounts.sol_vault.lamports();
    // Update vault lamports in pool accounting
    ctx.accounts.pool.sol_vault_lamports = ctx.accounts.pool.sol_vault_lamports
        .checked_add(after_vault_lamports
            .checked_sub(before_vault_lamports)
            .ok_or(LiquidUnstakerErrorCode::MathUnderflow)?)
        .ok_or(LiquidUnstakerErrorCode::MathOverflow)?;
}
```

**Impact:** If the `stake_account` has rewards, prematurely splitting the `stake_account` to exit the vault would benefit the withdrawer and cause the vault to lose rewards. The second impact is that when a malicious user donates less than `minimum_delegation_amount` the `split(...)` CPI will fail preventing successful full withdrawals.

**Recommendation:** When `ctx.accounts.stake_account_info_source.stake_lamports = 0`, only close it if the `stake_account` has no lamports. Solving the reward dilution issue is not easy, so it is recommended to consider whether to keep the `withdraw_stake_account(...)` instruction.

**Status:** Fixed

**Update from The Vault:** Resolved in [575250e813947cd86a83bdcdb8fe23c02ebd67e6](https://github.com/SolanaVault/liquid-unstaker/commit/575250e813947cd86a83bdcdb8fe23c02ebd67e6) and [ade63ba7116618dda6ad9a54327bfcd899edd813](https://github.com/SolanaVault/liquid-unstaker/commit/ade63ba7116618dda6ad9a54327bfcd899edd813).
