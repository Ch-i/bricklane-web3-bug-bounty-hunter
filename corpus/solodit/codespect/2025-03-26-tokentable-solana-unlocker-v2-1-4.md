---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-1-4
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[L-05] Withdrawals from Fee Collector become impossible after renouncing ownership'
vuln_class: []
---

# [L-05] Withdrawals from Fee Collector become impossible after renouncing ownership

_Section severity (from Solodit section header): Low_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Files:** [`renounce_ownership.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/renounce_ownership.rs)

**Description:**

The `renounce_ownership` instruction in the Fee Collector program is available for the owner. The following instructions become impossible to call when ownership is renounced:

- `init_fee_token`;
- `set_custom_fee_bips`;
- `set_custom_fee_fixed`;
- `set_default_fee`;
- `transfer_ownership`;
- `withdraw`;

There are two major consequences to the protocol when ownership is renounced:

- The whole protocol will operate normally for existing unlockers, however, new ones could not have their own fee accounts, hence all fees will fallback to the default fee: `storage.default_fees_bips`;
- It will be impossible to withdraw fees;

**Impact:** Withdrawals shall be blocked if ownership is renounced.

**Recommendation:** Specify what the ownership renouncement should block from happening or remove the instruction for safety reasons.

**Status:** Fixed

**Update from TokenTable:** Removed `renounce_ownership()` in [e8c372dbee51e66a152f6683d002dbc2e297a07b](https://github.com/EthSign/tokentable-unlocker-solana/tree/e8c372dbee51e66a152f6683d002dbc2e297a07b).
