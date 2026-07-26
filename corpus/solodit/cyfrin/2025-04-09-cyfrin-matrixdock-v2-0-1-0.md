---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Only emit events when state actually changes
vuln_class: []
---

# Only emit events when state actually changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** Only emit events when state actually changes, for example in `MTokenMessager::setAllowedPeer`:
```diff
    function setAllowedPeer(
        uint64 chainSelector,
        address messager,
        bool allowed
    ) external onlyOwner {
+      require(chainSelector][messager] != allowed, "No state change");
       allowedPeer[chainSelector][messager] = allowed;
       emit AllowedPeer(chainSelector, messager, allowed);
    }
```

Also affects:
* `MTokenMessagerV2::setAllowedPeer`

**Matrixdock:** Acknowledged.
