---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Don't initialize to default values
vuln_class: []
---

# Don't initialize to default values

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Don't initialize to default values:

File: `src/DropBox.sol`
```solidity
142:    isEarnmClaimAllowed = false;
143:    isRevealAllowed = false;
265:      for (uint32 i = 0; i < boxAmount; i++) {
424:    uint256 amountToClaim = 0;
437:    for (uint256 i = 0; i < _boxIds.length; i++) {
478:    for (uint256 i = 0; i < _boxIds.length; i++) {
537:    for (uint256 i = 0; i < _randomWords.length; i++) {
620:    for (uint32 i = 0; i < boxAmount; i++) {
676:    uint256 totalLiability = 0;
784:    for (uint256 i = 0; i < boxIds.length; i++) {
```

**Mode:**
Fixed in commit [16ecc3b](https://github.com/Earnft/dropbox-smart-contracts/commit/16ecc3ba4ef8463d6b805d8ad95a7fa15c96d0db).

**Cyfrin:** Verified.
