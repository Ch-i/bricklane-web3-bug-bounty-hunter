---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-08-15-cyfrin-earnm-dropbox-v2-0-4-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-08-15T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md
tags:
- firm:cyfrin
- report:2024-08-15-cyfrin-earnm-dropbox-v2-0
title: Enforce ascending order for boxIds to implement more efficient duplicate prevention
  in `DropBox::claimDropBoxes`
vuln_class: []
---

# Enforce ascending order for boxIds to implement more efficient duplicate prevention in `DropBox::claimDropBoxes`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-08-15-cyfrin-earnm-dropbox-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-08-15-cyfrin-earnm-dropbox-v2.0.md)_

---

**Description:** Enforce ascending order for boxIds to implements more efficient duplicate prevention in `DropBox::claimDropBoxes`:
```diff
-      for (uint256 j = i + 1; j < _boxIds.length; j++) {
-        if (_boxIds[i] == _boxIds[j]) revert BadRequest();
-      }
+     if(i > 0 && _boxIds[i-1] >= _boxIds[i]) revert BadRequest();
```

**Mode:**
Fixed in commit [756fc82](https://github.com/Earnft/dropbox-smart-contracts/commit/756fc827eb5265c09e7e1eca8c7a55832e58d1f2).

**Cyfrin:** Verified.
