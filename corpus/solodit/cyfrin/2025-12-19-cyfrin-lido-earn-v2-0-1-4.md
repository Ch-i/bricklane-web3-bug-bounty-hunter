---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-19-cyfrin-lido-earn-v2-0-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-12-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-19-cyfrin-lido-earn-v2-0
title: '`nonReentrant` is not the first modifier'
vuln_class: []
---

# `nonReentrant` is not the first modifier

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-19-cyfrin-lido-earn-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-19-cyfrin-lido-earn-v2.0.md)_

---

**Description:** `EmergencyVault::emergencyWithdraw` and `EmergencyVault::activateRecovery` place `nonReentrant` as the second modifier rather than first. To protect against reentrancy in other modifiers, the `nonReentrant` modifier should be the first modifier in the list of modifiers.

**Lido:** Fixed in commit [`3d89267`](https://github.com/lidofinance/defi-interface/commit/3d89267ee409eb0857abb9302dcc42337429e4f9)

**Cyfrin:** Verified.
