---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0-2-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-17T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-17-cyfrin-securitize-solana-spl-acl-v2-0
title: Unnecessary mut constraint on mint in read-only ops delays genuine operations
  that require mint to be mutable
vuln_class: []
---

# Unnecessary mut constraint on mint in read-only ops delays genuine operations that require mint to be mutable

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-17-cyfrin-securitize-solana-spl-acl-v2.0.md)_

---

**Description:** Several instructions mark the `mint` account as mutable when they only read from it, wasting compute on unnecessary write-lock acquisition. While the cu itself may not be the problem, but users trying to interact with instructions that actually modifies mint's state and hence require mint to be mutably passed may face delays for no reasons because once an account is passed as mutable in one instruction, it can't be passed as mutable in another until the prev instruction goes by. for eg. `mint_to_checked` instruction requires mint account to be mutable because it is genuinely modifying mint state, but `set_gating_program` is not modifying any state on mint and only needs it for validation, it makes sense to pass mint account as readable here so that other instructions like `mint_to_checked` does not face delays.

**Impact:** Unnecessary delay on genuine ops that actually modify mint.

**Recommended Mitigation:** Remove the `mut` constraint from mint. Here are the instances:
1. set_gating_program.rs
2. toggle_permissionless.rs


**Securitize:** Fixed in [5d87019](https://github.com/securitize-io/bc-solana-spl-acl-sc/commit/5d8701920450b743ef8ab54c1ef77136e5f34dbe).

**Cyfrin:** Verified.

\clearpage
