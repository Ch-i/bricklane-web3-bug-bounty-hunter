---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-1-2
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: A single unrecoverable Receipt atom permanently disables sweep
vuln_class: []
---

# A single unrecoverable Receipt atom permanently disables sweep

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::sweep` is the only way to recover tokens held above the amount required to back Receipt holders, but it reverts whenever `totalSupply() != 0`.

Receipts can be transferred to any address, including the Receipt contract itself. If a holder sends one Receipt atom there, the contract cannot redeem or burn it, so total supply can never return to zero. Every later `sweep` then reverts, even for balances that are provably unrelated to holder claims, such as donations, rounding residue, or accepted transfer over-delivery.

**Impact:** A griefer can permanently disable surplus recovery for the cost of one Receipt atom and gas. The attacker cannot withdraw the stranded assets, and normal holder backing and redemptions remain solvent, so the impact is limited to a cheap denial of the rescue mechanism.

**Recommended Mitigation:** Allow the owner to sweep only the portion of the collateral or consideration balance that exceeds the amount required to back outstanding Receipts. Keep other tokens gated on zero supply and document that tokens sharing a balance ledger are unsupported.

**GreekFi:** Fixed in [PR47](https://github.com/greekfi/contracts/pull/47)

**Cyfrin:** Verified. Receipt now limits live-supply sweeps to balances above the collateral and consideration backing required by outstanding Receipts, so a stranded Receipt atom no longer disables recovery of fees, donations, or foreign tokens.
