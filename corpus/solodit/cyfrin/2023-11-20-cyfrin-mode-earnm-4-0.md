---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-0
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
title: Remove from storage `baseMetadataURI` as already stored in `ERC1155` and `name`
  as never used
vuln_class: []
---

# Remove from storage `baseMetadataURI` as already stored in `ERC1155` and `name` as never used

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Remove from [storage](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L53-L54) `baseMetadataURI` as already stored in `ERC1155` & `name` as never used.

**Impact:** Extra storage costs and extra gas to write these unnecessary values to storage.

**Recommended Mitigation:** Remove both `baseMetadataURI` & `name` from storage.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.
