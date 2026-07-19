---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-4-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Use timestamp instead of uri length to test of existing document in `DocumentManager`
vuln_class: []
---

# Use timestamp instead of uri length to test of existing document in `DocumentManager`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** Use timestamp instead of uri length to test of existing document in `DocumentManager`:
```diff
-       if (bytes($._documents[docHash].docURI).length == 0)
-           revert EmptyDocument();
+       if ($._documents[docHash].timestamp == 0) revert EmptyDocument();
```

**Remora:** Fixed in commit [77af634](https://github.com/remora-projects/remora-smart-contracts/commit/77af634d953ce3549a33e7b34db924233dc7689a).

**Cyfrin:** Verified.

\clearpage
