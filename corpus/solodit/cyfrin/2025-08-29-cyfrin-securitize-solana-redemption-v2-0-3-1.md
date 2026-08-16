---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-29-cyfrin-securitize-solana-redemption-v2-0-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-29-cyfrin-securitize-solana-redemption-v2-0
title: Missing Two Step Ownership And Authority Transfer Validation
vuln_class: []
---

# Missing Two Step Ownership And Authority Transfer Validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-29-cyfrin-securitize-solana-redemption-v2.0.md)_

---

**Description:** Both `change_admin_handler` and `change_liquidity_withdraw_authority_handler` directly reassign critical control fields (`off_ramp_state.admin` and `off_ramp_state.liquidity_withdraw_authority`) in a single transaction without requiring confirmation from the proposed new key. This one-step transfer model increases the risk of accidental misconfiguration or malicious key injection. Additionally, neither function validates against assignment of the default zero address (`Pubkey::default()`), which could permanently lock the system by assigning an unusable authority.

**Impact:** If a privileged signer mistakenly or maliciously sets the new authority to the default address, administrative or liquidity withdrawal rights could be irreversibly lost. Furthermore, the absence of a two-step acceptance process enables unilateral transfers without the consent of the intended new owner, reducing operational safety and creating potential governance disputes.

**Recommended Mitigation:**
- Introduce a two-step transfer process where the current owner proposes a new authority, and the proposed authority must explicitly accept before finalization.
- Also, enforce non-default key validation to prevent assignment to the zero address.


**Securitize:** Acknowledged.
