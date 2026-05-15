---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-10
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-11] Inconsitent usage of `MIN_POSSIBLE_ANNUAL_INTEREST_RATE`'
vuln_class: []
---

# [L-11] Inconsitent usage of `MIN_POSSIBLE_ANNUAL_INTEREST_RATE`

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The variable `MIN_POSSIBLE_ANNUAL_INTEREST_RATE` is being used instead of `MIN_ANNUAL_INTEREST_RATE`


However some parts of the codebase still refer to `MIN_ANNUAL_INTEREST_RATE`


**Mitigation**

Clean up the codebase to consistently use `MIN_POSSIBLE_ANNUAL_INTEREST_RATE`
