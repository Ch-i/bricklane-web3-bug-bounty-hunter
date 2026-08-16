---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Remove redundant `tierId` validity check from `DropBox::claimDropBoxes`
vuln_class: []
---

# Remove redundant `tierId` validity check from `DropBox::claimDropBoxes`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** `DropBox::claimDropBoxes` performs this check before calling `DropBoxFractalProtocol::_calculateVestingPeriodPerBox`:
```solidity
// [Safety check] Validate that the box tier is valid
if (!(box.tier > 0 && box.tier <= TIER_IDS_LENGTH)) revert InvalidTierId();
```

However `DropBoxFractalProtocol::_calculateVestingPeriodPerBox` performs the same check, hence this check is redundant and should be removed from `DropBox::claimDropBoxes`.

**Mode:**
Fixed in commit [7ebd568](https://github.com/Earnft/dropbox-smart-contracts/commit/7ebd5682e5263ce42a0432548e4b7ed5b801b7be).

**Cyfrin:** Verified.
