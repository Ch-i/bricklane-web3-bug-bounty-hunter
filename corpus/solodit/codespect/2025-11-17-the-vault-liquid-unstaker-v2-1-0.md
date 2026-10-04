---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-11-17-the-vault-liquid-unstaker-v2-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-11-17T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md
tags:
- firm:codespect
- report:2025-11-17-the-vault-liquid-unstaker-v2
title: '[H-01] The withdraw_stake_account(...) instruction does not assign the StakeAccount
  authority to the user'
vuln_class: []
---

# [H-01] The withdraw_stake_account(...) instruction does not assign the StakeAccount authority to the user

_Section severity (from Solodit section header): High_  
_Audit firm: CODESPECT_  
_Source report: [2025-11-17-The-Vault-Liquid-Unstaker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-11-17-The-Vault-Liquid-Unstaker-V2.md)_

---

**Files:** [`withdraw_stake_account.rs`](https://github.com/SolanaVault/liquid-unstaker/blob/2dd71f5e3d9017504783c67bc1b903ecaa169a54/programs/liquid-unstaker/src/instructions/withdraw_stake_account.rs#L171)

**Description:**

The `withdraw_stake_account(...)` instruction allows users to burn shares even when the vault has insufficient available funds. It splits a `StakeAccount` that has not yet been deactivated into a new `StakeAccount` containing the corresponding amount of SOL, enabling an immediate withdrawal. However, after splitting the `StakeAccount` via `stake_split(...)`, the authority of the newly created `StakeAccount` is not assigned to the user, preventing them from operating the split account.

**Impact:** The user burns their shares through `withdraw_stake_account(...)` but does not receive any accessible funds, and the program is also unable to operate on those funds. As a result, this portion of funds becomes stuck.

**Recommendation:** It is recommended to assign the authority of the `StakeAccount` split through `stake_split(...)` to the user.

**Status:** Fixed

**Update from The Vault:** Resolved in [e3a457993390529b803800375a3b6b493e975e5a](https://github.com/SolanaVault/liquid-unstaker/commit/e3a457993390529b803800375a3b6b493e975e5a).
