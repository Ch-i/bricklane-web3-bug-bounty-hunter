---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-4
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
title: Initialize `DropBox::boxIdCounter` to 1 avoiding default initialization to
  0
vuln_class: []
---

# Initialize `DropBox::boxIdCounter` to 1 avoiding default initialization to 0

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Initialize `DropBox::boxIdCounter` to 1 avoiding default initialization to 0:

```diff
- uint256 internal boxIdCounter; // Counter for the box ids, starting from 1 (see _assignTierAndMint function)
+ uint256 internal boxIdCounter = 1; // Counter for the box ids
```

And change this line in `_assignTierAndMint`:

```diff
- uint256 newBoxId = ++boxIdCounter;
+ uint256 newBoxId = boxIdCounter++;
```

**Mode:**
Fixed in commit [4e2d90b](https://github.com/Earnft/dropbox-smart-contracts/commit/4e2d90b7f18c3bcc3810754941e460bbe6894189).

**Cyfrin:** Verified.
