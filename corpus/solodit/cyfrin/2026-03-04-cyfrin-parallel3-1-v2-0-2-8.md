---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-04-cyfrin-parallel3-1-v2-0-2-8
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-04T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-04-cyfrin-parallel3-1-v2-0
title: Deploy script `UpdateParallelizer.ts` does not handle facet removal case
vuln_class: []
---

# Deploy script `UpdateParallelizer.ts` does not handle facet removal case

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-04-cyfrin-parallel3.1-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-04-cyfrin-parallel3.1-v2.0.md)_

---

**Description:** When upgrading the script finds all the selectors that should be _added_ (`FaceCutAction.Add`) or _replaced_ (`Replace`) but the
case for `Remove` is missing.  This could lead to deleted selectors being present after an upgrade. This would mean that users could still call these endpoints and have them `delegatecall` to the old implementation, which may not be what was intended.

**Impact:** The impact depends entirely on what selectors would not be removed.

**Parallel:** Fixed in commit [c340795](https://github.com/parallel-protocol/parallel-parallelizer/commit/c340795ad0ecc071ff202447d67540e9943f15fd).

**Cyfrin:** Verified. `UpdateParallelizer.ts` now accounts for the case when removing selectors from the old facet.
