---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-1-1
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
title: '[L-02] Lack of token_mint validation in the Deposit instruction'
vuln_class: []
---

# [L-02] Lack of token_mint validation in the Deposit instruction

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`deposit.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/deposit.rs)

**Description:**

The Deposit instruction in the Unlocker program is used by the owner of the unlocker account to deposit the initial amount of tokens for later claiming. When this instruction is called for the first time a new vault account is created for a specified `token_mint` account to hold the assets tied to the specific unlocker account (identified by `_project_id`). The Deposit instruction can be called by anyone as there is no validation of the owner.

A malicious user could call the Deposit instruction and provide a junk `token_mint` account and hence a vault tied to that unlocker will be created. Further deposits of the intended SPL token become impossible because the vault is already created and the entire unlocker becomes useless.

**Impact:** Malicious user could DoS a created unlocker account before the initial funds are deposited. No funds are lost, but another unlocker needs to be created for the owner by the program’s owner.

**Recommendation:** Validate the provided `token_mint` against the `unlocker.project_token` either through Anchor context definition (recommended for clarity) or inside the handler.

**Status:** Fixed

**Update from TokenTable:** Added `token_mint` constraint in [6bccb7d0ebefd3cdaaa82278c9b0567c4f01f13e](https://github.com/EthSign/tokentable-unlocker-solana/tree/6bccb7d0ebefd3cdaaa82278c9b0567c4f01f13e).
