---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-2-4
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-03-26T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md
tags:
- firm:codespect
- report:2025-03-26-tokentable-solana-unlocker-v2
title: '[I-05] Missing check for fee_collector in Unlocker account initialization'
vuln_class: []
---

# [I-05] Missing check for fee_collector in Unlocker account initialization

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Original severity:** Best Practices

**Files:** [`initialize.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/initialize.rs#L22)

**Description:**

The Unlocker account stores the `fee_collector` field, which is initialized in the `initialization()` instruction and cannot be modified afterward. If an incorrect `fee_collector` is provided during initialization, it will be permanently set, preventing any future changes.

**Impact:** For this Unlocker is will be impossible to claim tokens through the `claim()` instruction.

**Recommendation:** It is recommended to check whether `fee_collector` is the expected account address during the `initialization()` instruction.

**Status:** Fixed

**Update from TokenTable:** Added the ability to change the `fee_collector` for a project rather than adding verification in [a80d3c31d](https://github.com/EthSign/tokentable-unlocker-solana/tree/a80d3c31d16dc5e02c8995dac62d4bc0e7b0bf54). We may need to change this address at some point in the future. This function is only callable by an admin (read: one of our wallet accounts), so errors should not happen in setting these values, and we would be able to fix any errors if need be.
