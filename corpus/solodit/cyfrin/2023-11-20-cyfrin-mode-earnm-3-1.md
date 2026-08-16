---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-3-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: '`MysteryBox::claimMysteryBoxes()` should return custom error when reverting
  due to `amountToClaim == 0`'
vuln_class: []
---

# `MysteryBox::claimMysteryBoxes()` should return custom error when reverting due to `amountToClaim == 0`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** `MysteryBox::claimMysteryBoxes()` should [return custom error](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L305) when reverting due to `amountToClaim == 0`. Currently it returns `InsufficientEarnmBalance` which is the same error as if the contract had insufficient token balance for the mystery box being redeemed.

**Impact:** Misleading error is returned.

**Recommended Mitigation:** Return a custom error.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.
