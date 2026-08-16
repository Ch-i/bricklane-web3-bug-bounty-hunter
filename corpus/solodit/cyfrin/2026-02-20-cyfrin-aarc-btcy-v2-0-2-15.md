---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-15
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: '`nonReentrant` is not the first modifier on `IBTCYHub::processSubscriptions`
  / `processRedemptions`'
vuln_class: []
---

# `nonReentrant` is not the first modifier on `IBTCYHub::processSubscriptions` / `processRedemptions`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCYHub::processSubscriptions` and `processRedemptions` apply `nonReentrant` after other modifiers. While this does not change correctness in Solidity, best practice is to place `nonReentrant` first to prevent possible reentrancy in other modifiers.

Consider reordering modifiers so `nonReentrant` is the first modifier on both functions.

**Aarc:** Fixed in commit [a2fb621](https://github.com/aarc-xyz/btcy-contracts-main/commit/a2fb6213a1e2a90977c6ef3edc7c0bdaee2c8540).

**Cyfrin:** Verified.
