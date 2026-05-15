---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-12
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-13] `SwapOperations` Swap Fees may add up to more than 100%'
vuln_class: []
---

# [L-13] `SwapOperations` Swap Fees may add up to more than 100%

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`swapBaseFee` is capped to 1e18, but it is added to `Pair.getSwapFee` meaning that it may result in a value higher than 100%



**Mitigation**

Cap fees at a smaller value, such as at most 10%
