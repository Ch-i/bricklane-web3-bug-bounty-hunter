---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Loop backwards in `MysteryBox::_determineTier()` to avoid multiple variables
  and simplify code
vuln_class: []
---

# Loop backwards in `MysteryBox::_determineTier()` to avoid multiple variables and simplify code

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** [Loop backwards](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L380-L383) in `MysteryBox::_determineTier()` to avoid multiple variables and simplify code.

**Impact:** Gas optimization and simpler code.

**Recommended Mitigation:** See description.

**Mode:**
Fixed in commit [4d56069](https://github.com/Earnft/smart-contracts/commit/4d560697f7dd6fa4f6b6303cca3e21c4025bee5b).

**Cyfrin:** Verified.
