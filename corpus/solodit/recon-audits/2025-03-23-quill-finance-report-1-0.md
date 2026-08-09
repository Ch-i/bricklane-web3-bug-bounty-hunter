---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-0
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
title: '[L-01] Long enough sequencer shutdown can create undefined shutdown risk'
vuln_class: []
---

# [L-01] Long enough sequencer shutdown can create undefined shutdown risk

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

48 hours + no update = Shutdown

48 hours + update = No shutdown

Almost 48 hours + Block stuffing could be used to effectively have a 48 hours delay

All of these can either cause a shutdown or a no-op

**Mitigation**

I don't believe the issue can be mitigated, in case of that big a sequencer downtime, only Scroll will be able to decide what to do

If you can ensure that the oracles update will be processed before user operations then this can prevent branch shutdowns
