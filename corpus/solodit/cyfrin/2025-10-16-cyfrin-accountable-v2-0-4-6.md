---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-16-cyfrin-accountable-v2-0-4-6
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-16-cyfrin-accountable-v2-0
title: '`nonReentrant` is not the first modifier'
vuln_class: []
---

# `nonReentrant` is not the first modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-16-cyfrin-accountable-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-16-cyfrin-accountable-v2.0.md)_

---

**Description:** In `FeeManager::withdrawProtocolFee`, `nonReentrant` is not the first modifier. To protect against reentrancy in other modifiers, the `nonReentrant` modifier should be the first modifier in the list of modifiers. Consider putting `nonReentrant` first for consistent reentrancy protection.

**Accountable:** Fixed in commit [`c7f31b5`](https://github.com/Accountable-Protocol/credit-vaults-internal/commit/c7f31b51fc1bfb4fe96450a189751f6f72d8274d)

**Cyfrin:** Verified.
