---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-3-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Prevent duplicate `boxId` inputs to `MysteryBox::claimMysteryBoxes()`
vuln_class: []
---

# Prevent duplicate `boxId` inputs to `MysteryBox::claimMysteryBoxes()`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Consider preventing duplicate `boxId` inputs to [`MysteryBox::claimMysteryBoxes()`](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L271) as this may be exploitable under certain circumstances.

**Impact:** Attackers could use duplicate inputs to exploit token claiming.

**Recommended Mitigation:** Revert if duplicate inputs occur; `boxId` is unique so duplicate inputs are an obvious sign of a malicious attack.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3), [3713107](https://github.com/Earnft/smart-contracts/commit/3713107bb24382bda0fb6ac2eb51e9c64c39c98d).

**Cyfrin:** Verified.
