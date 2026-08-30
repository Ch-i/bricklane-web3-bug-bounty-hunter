---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-0-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Incorrect cap on `batchesAmount` results in 500M instead of 5B tokens distributed
  to mystery box holders
vuln_class: []
---

# Incorrect cap on `batchesAmount` results in 500M instead of 5B tokens distributed to mystery box holders

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** `setBatchesAmount()` [caps](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L782) the maximum `batchesAmount` 100 but this is incorrect. Every batch releases mystery boxes which can be redeemed for ~5M tokens and there are 5B tokens in total so 1000 batches to distribute the entire supply.

**Impact:** Incorrectly capping to 100 batches results in never being able to distribute all 5B tokens, but only 500M tokens.

**Recommended Mitigation:** Cap `batchesAmount` to 1000 to allow full token distribution.

**Mode:**
Fixed in commit [ae3dc68](https://github.com/Earnft/smart-contracts/commit/ae3dc68db8c723293df01cb14297dc3264a21dbe).

**Cyfrin:** Verified.

\clearpage
