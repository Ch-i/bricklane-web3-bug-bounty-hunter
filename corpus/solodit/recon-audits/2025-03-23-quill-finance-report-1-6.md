---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-07] BATCH DEBT FIXES - Rebase is economicall unfeasible'
vuln_class: []
---

# [L-07] BATCH DEBT FIXES - Rebase is economicall unfeasible

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

```python
SHARES * 1e16 // DENOM
9999999.0
SHARES * 1e14 // DENOM
99999.0
SHARES * 1e13 // DENOM
9999.0
SHARES * 1e9 // DENOM
1.0
SHARES * 1e8 // DENOM
0.0
SHARES * 1e10 // DENOM
10.0
SHARES * 2e8 // DENOM
0.0
SHARES * 9e8 // DENOM
0.0
SHARES * 1.9e8 // DENOM
0.0
SHARES * 1.9e9 // DENOM
1.0
0.06 * 1e9 / 1e18
6e-11
0.06 * 1e9 / 1e18 * 3463
2.0778e-07
0.06 * 1e9 / 1e18 * 3463 * 300_000
0.062334
0.06 * 1e9 / 1e18 * 3463 * 300_00
0.0062334
0.06 * 1e9 / 1e18 * 3463 * 3000
0.00062334
1e9 / 1e18 * 3463
3.463e-06
```
