---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-4
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
title: '[L-05] `SwapERC20` Hardcoded DOMAIN_SEPARATOR will cause issues and replay
  on a chain split'
vuln_class: []
---

# [L-05] `SwapERC20` Hardcoded DOMAIN_SEPARATOR will cause issues and replay on a chain split

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

**DOMAIN_SEPARATOR** being hardcoded will either:
- Stop working if the chain hardforks with a new ID
- Will open up for replays if the chain forks

**Mitigation**

The code in `DebtToken` already deals with these issues, you can re-use that
