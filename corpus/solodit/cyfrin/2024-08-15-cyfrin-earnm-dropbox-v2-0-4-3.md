---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Remove `< 0` checks for unsigned variables since they can't be negative
vuln_class: []
---

# Remove `< 0` checks for unsigned variables since they can't be negative

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Remove `< 0` checks for unsigned variables since they can't be negative:

File: `src/DropBox.sol`
```solidity
538:      if (_randomWords[i] <= 0) revert InvalidRandomWord();
```

**Mode:**
Fixed in commit [ccc358a](https://github.com/Earnft/dropbox-smart-contracts/commit/ccc358a88e27ed08c85a37c7770af4dea24f9155).

**Cyfrin:** Verified.
