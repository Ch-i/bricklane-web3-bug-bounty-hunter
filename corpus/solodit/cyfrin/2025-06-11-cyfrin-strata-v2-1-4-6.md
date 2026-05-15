---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-4-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Remove unused return value from `pUSDeVault::stakeUSDe` and explicitly revert
  if `USDeAssets == 0`
vuln_class: []
---

# Remove unused return value from `pUSDeVault::stakeUSDe` and explicitly revert if `USDeAssets == 0`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Remove unused return value from `pUSDeVault::stakeUSDe` and explicitly revert if `USDeAssets == 0`.

**Strata:** Fixed in commit [513d589](https://github.com/Strata-Money/contracts/commit/513d5890771d9bbe520740ef8f26a24931bf5590).

**Cyfrin:** Verified.
