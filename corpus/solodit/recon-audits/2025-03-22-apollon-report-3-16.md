---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-16
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-17] `_getCurrentPythResponse` can benefit by having more validation'
vuln_class: []
---

# [L-17] `_getCurrentPythResponse` can benefit by having more validation

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Pyth works as follows:
- It returns an integer
- It returns an exponent by which to scale the integer for the price
- it returns the publishTime
- and a confidence interval

The reason why Pyth includes a confidence interval is due to the impossibility of chosing a single price that is the "correct" price

**Mitigation**

Consider implementing additional checks, you could take inspiration from Euler's multi-audited feeds:
https://github.com/euler-xyz/euler-price-oracle/blob/master/src/adapter/pyth/PythOracle.sol
