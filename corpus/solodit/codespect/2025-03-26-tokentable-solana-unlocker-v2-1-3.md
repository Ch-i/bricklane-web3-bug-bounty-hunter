---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-1-3
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[L-04] Missing the is_withdrawable check in the withdraw_deposit(...) instruction'
vuln_class: []
---

# [L-04] Missing the is_withdrawable check in the withdraw_deposit(...) instruction

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`withdraw_deposit.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/withdraw_deposit.rs)

**Description:**

In the Unlocker account, `is_withdrawable` is set to control whether the unlocker owner is allowed to withdraw tokens from the vault. However, the `withdraw_deposit()` instruction does not check the `is_withdrawable` field, causing the unlocker owner’s withdrawals to be always allowed.

**Impact:** The unlocker owner’s withdrawals will not be controlled by the `is_withdrawable` field.

**Recommendation:** Add the `is_withdrawable` check in the `withdraw_deposit()` instruction.

**Status:** Fixed

**Update from TokenTable:** Added `is_withdrawable` check to the `withdraw_deposit()` function in commit [e8521cef](https://github.com/EthSign/tokentable-unlocker-solana/tree/e8521cef9ff2aa88546d3ceba27c414178863c36).
