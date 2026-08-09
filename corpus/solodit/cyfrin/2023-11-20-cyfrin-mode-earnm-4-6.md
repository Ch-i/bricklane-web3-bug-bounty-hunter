---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Remove unused `category` from `MysteryBox::_calculateVestingPeriodPerBox()`
vuln_class: []
---

# Remove unused `category` from `MysteryBox::_calculateVestingPeriodPerBox()`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Remove [unused](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L296) `category` from `MysteryBox::_calculateVestingPeriodPerBox()`.

**Impact:** Gas optimization & simpler, cleaner code.

**Recommended Mitigation:** See description.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.
