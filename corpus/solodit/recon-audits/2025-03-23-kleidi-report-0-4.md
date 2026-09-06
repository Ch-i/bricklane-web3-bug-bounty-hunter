---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-05] Refactoring - `Timelock` wildcard and non wildcard checks could be
  simplified'
vuln_class: []
---

# [L-05] Refactoring - `Timelock` wildcard and non wildcard checks could be simplified

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Refactoring Analysis**

Fundamentally:
You either accept all (wildcard)
Or you check some
And checking some is tied to exact matches on some pieces

Each bytes check has a list of values afaict

So there is prob some risk there
But also not sure if it can be avoidable


In TS
Check {
    isWildcard: boolean,
    actualChecks: Check[]
}

Where each check is the segmented check


Start
End
Self Address Check
Data
