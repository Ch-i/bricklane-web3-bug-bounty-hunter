---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-23-cyfrin-soneium-shibuya-v2-0-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-12-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-23-cyfrin-soneium-shibuya-v2-0
title: Missing zero amount validation in crosschain operations
vuln_class: []
---

# Missing zero amount validation in crosschain operations

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-23-cyfrin-soneium-shibuya-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-23-cyfrin-soneium-shibuya-v2.0.md)_

---

**Description:** The `crosschainMint()` and `crosschainBurn()` functions don't validate for zero amounts, which could lead to unnecessary event emissions.

**Recommended Mitigation:** Add zero amount checks and revert if amount is zero.

**Startale:** Fixed in commit [fa77e9](https://github.com/StartaleLabs/ccip-contracts-registration/commit/fa77e9745ed943ba940a6523b441a67111355c1c).

**Cyfrin:** Verified.
