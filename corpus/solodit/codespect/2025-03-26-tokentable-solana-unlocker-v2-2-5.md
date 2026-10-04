---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-03-26-tokentable-solana-unlocker-v2-2-5
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
title: '[I-06] Missing check to verify if the fields stored in the Account are consistent
  with the seed'
vuln_class: []
---

# [I-06] Missing check to verify if the fields stored in the Account are consistent with the seed

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-03-26-TokenTable-Solana-Unlocker-V2.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-03-26-TokenTable-Solana-Unlocker-V2.md)_

---

**Original severity:** Best Practices

**Files:** [`create_preset.rs`](https://github.com/EthSign/tokentable-unlocker-solana/blob/7516b8c86cb305f9d9eb3ac77e7fcd7c6b60cc2f/programs/unlocker-v2-solana/src/instructions/create_preset.rs#L40)

**Description:**

The `PresetAccount` stores the `project_id` field, and the `ActualAccount` stores both the `project_id` and `actual_id` fields. The protocol does not check whether these stored fields match the fields used to generate the seed during account initialization.

**Impact:** No on-chain impact, but off-chain parsing may result in mismatched data in the account.

**Recommendation:** It is recommended to check whether the relevant fields in the `Preset` struct and `Actual` struct match.

**Status:** Fixed

**Update from TokenTable:** Added checks to ensure relevant fields match in Preset and Actual structs in [2079107e](https://github.com/EthSign/tokentable-unlocker-solana/tree/2079107edcd5d2294ac969945b86b543a256283e).

**Update from CODESPECT:** An unnecessary duplicated `project_id` argument is added to the instruction while the same value is present in the actual struct argument. The same goes for Preset creation.
