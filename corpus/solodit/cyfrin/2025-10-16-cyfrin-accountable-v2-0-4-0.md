---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: Prevent accidental ownership and admin renouncement
vuln_class: []
---

# Prevent accidental ownership and admin renouncement

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** The inherited `renounceOwnership()` and allow the last authority to remove themselves, potentially leaving the contract permanently ownerless or admin‑less, blocking critical functions.

Consider override `renounceOwnership()` in `TokenAirdrop` to always revert.

**Accountable:** Fixed in commit [`be75091`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/be7509165d468fd19bf48bab3fa87e565412a5b6)

**Cyfrin:** Verified.
