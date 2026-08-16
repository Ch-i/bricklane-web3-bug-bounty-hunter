---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Break out of loop once element has been deleted in `TokenBank::removeToken`
vuln_class: []
---

# Break out of loop once element has been deleted in `TokenBank::removeToken`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Break out of loop once element has been deleted in `TokenBank::removeToken`:
```diff
    function removeToken(address tokenAddress) external restricted {
        for (uint i = 0; i < developments.length; ++i) {
            if (developments[i] == tokenAddress) {
                address end = developments[developments.length - 1];
                developments[i] = end;
                developments.pop();
+               break;
            }
        }
```

**Remora:** Fixed as of latest commit 2025/07/02 but exact commit unknown.

**Cyfrin:** Verified.
