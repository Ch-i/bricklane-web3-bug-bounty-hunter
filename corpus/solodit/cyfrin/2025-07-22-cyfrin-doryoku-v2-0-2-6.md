---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-22-cyfrin-doryoku-v2-0-2-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-22T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-22-cyfrin-doryoku-v2-0
title: Same Conditions Revalidated in Instruction Logic and Account Contexts
vuln_class: []
---

# Same Conditions Revalidated in Instruction Logic and Account Contexts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-22-cyfrin-doryoku-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-22-cyfrin-doryoku-v2.0.md)_

---

**Description:** In the `clmm_lp_farming` program, certain validations are performed twice: once in functions, and once in account validations:
- `user_position_token_account.amount == 1` checked both in `stake_clmm_position` function and `StakeCLMMPosition` struct,
- `!stake.claimed` checked both in `withdraw_clmm_position` function and `WithdrawCLMMPosition` struct

**Recommended Mitigation:** Consider removing one of these validations to prevent code duplication.

**Doryoku:**
Fixed in [fad227e](https://github.com/Warlands-Nft/belo_clmm_lp_farming/commit/fad227e80c53e207a8836365ed0c8449a17f2992).

**Cyfrin:** Verified.
