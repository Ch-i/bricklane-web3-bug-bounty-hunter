---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-1-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Excess eth not refunded to user in `MysteryBox::revealMysteryBoxes()`
vuln_class: []
---

# Excess eth not refunded to user in `MysteryBox::revealMysteryBoxes()`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** `MysteryBox::revealMysteryBoxes()` [allows execution](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L196-L198) if `msg.value >= mintFee` but in the case where `msg.value > mintFee`, the extra eth gets sent to `operatorAddress` not refunded back to the user.

**Impact:** User loses excess eth above `mintFee`.

**Recommended Mitigation:** Either refund excess eth back to the user or revert if `msg.value != mintFee`.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.
