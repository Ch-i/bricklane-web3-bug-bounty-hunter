---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-08-cyfrin-strata-tranches-v2-0-4-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-08-cyfrin-strata-tranches-v2-0
title: Misleading variable name to set the `asset` for the `Tranche`
vuln_class: []
---

# Misleading variable name to set the `asset` for the `Tranche`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-08-cyfrin-strata-tranches-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-08-cyfrin-strata-tranches-v2.0.md)_

---

**Description:** The variable that is used to set the `asset` the `Tranche` will work with is named `stakedAsset`.
This is misleading because the two assets the system works with are `USDe` and `sUSDe`. ' sUSDe is the staked version of `USDe`, so the variable name can mislead people into thinking that the `asset` of the `Tranche` is expected to be `sUSDe` instead of `USDe`.

**Recommended Mitigation:** Rename the variable name to `baseAsset` or another name that doesn't have the word `stake` in the name.

**Strata:**
Fixed in commit [2d7f5a17](https://github.com/Strata-Money/contracts-tranches/commit/2d7f5a17e0ac1545506530e8ed85cad828f392f6).

**Cyfrin:** Verified.
