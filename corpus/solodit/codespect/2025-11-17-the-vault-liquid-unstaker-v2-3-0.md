---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-3-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[L-01] Inconsistent rent refund'
vuln_class: []
---

# [L-01] Inconsistent rent refund

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`liquid_unstake_stake_account.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/liquid_unstake_stake_account.rs#L155)

**Description:**

The `StakeAccount` authority and the LST holder can interact with the vault to assign a deactivating account to the pool and immediately withdraw SOL from the vault. This process requires the user to pay rent to create the `StakeAccountInfo` account. In the `liquid_unstake_stake_account(...)` instruction, the rent is not refunded. When the account is released, the rent goes to the vault. However, in the `liquid_unstake_lst(...)` and `liquid_unstake_lst_wrapped(...)` instructions, the vault reimburses the payer for the rent before the instruction ends.

**Impact:** The inconsistent refund logic may affect accounting consistency, predictability, and user experience.

**Recommendation:** It is recommended to standardize whether rent should be refunded.

**Status:** Fixed

**Update from The Vault:** Resolved in [00e927a9a3ceef5c3a4a4dccffefbb756c5f8216](https://github.com/SolanaVault/liquid-unstaker/commit/00e927a9a3ceef5c3a4a4dccffefbb756c5f8216).
