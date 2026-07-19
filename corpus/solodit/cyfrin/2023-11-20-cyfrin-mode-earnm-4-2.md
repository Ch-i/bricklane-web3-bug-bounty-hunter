---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md
tags:
- firm:cyfrin
- report:2023-11-20-cyfrin-mode-earnm
title: Simplify `boxId` storage mappings as `boxId` is unique to addresses and tiers
vuln_class: []
---

# Simplify `boxId` storage mappings as `boxId` is unique to addresses and tiers

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Since `boxId` is unique such that multiple address or tiers can never have the same `boxId`, at least [2 storage mappings](https://github.com/Earnft/smart-contracts/blob/43d3a8305dd6c7325339ed35d188fe82070ee5c9/contracts/MysteryBox.sol#L64-L65) could potentially be simplified: `addressToTierToBoxIdToBlockTs` & `addressToBoxIdToTier`.

Consider refactoring the other nested mappings to simplify and reduce complexity.

**Impact:** The storage mappings are already quite complex which is error-prone and the way these 2 are implemented will require more gas to read/write.

**Recommended Mitigation:** Simplify these mappings by taking advantage of the fact that `boxId` is unique to addresses & tiers.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3), [efa8199](https://github.com/Earnft/smart-contracts/commit/efa8199895c7f5c76b5ac3c81bceaa94c8838eb2), [9c5ac66](https://github.com/Earnft/smart-contracts/commit/9c5ac662180602a3b1addf57c791e562c0ab9cd7).

**Cyfrin:** Verified.
