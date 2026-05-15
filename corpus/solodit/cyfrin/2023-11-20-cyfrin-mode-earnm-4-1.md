---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-11-20-cyfrin-mode-earnm-4-1
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
title: Standardize `tierId` to either `uint8` or `uint256` avoiding constant conversions
  back and forth
vuln_class: []
---

# Standardize `tierId` to either `uint8` or `uint256` avoiding constant conversions back and forth

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-11-20-cyfrin-mode-earnm.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-11-20-cyfrin-mode-earnm.md)_

---

**Description:** Standardize `tierId` to either `uint8` or `uint256` avoiding constant conversions back and forth.

**Impact:** Having different types for `tierId` means it has to be converted but also increases complexity and confusion as to why it is different in some places to others.

**Recommended Mitigation:** Standardize `tierId` to either `uint8` or `uint256`.

**Mode:**
Fixed in commit [85b2012](https://github.com/Earnft/smart-contracts/commit/85b20121604b5d162bb14c2c96731b8345ca1cb3).

**Cyfrin:** Verified.
