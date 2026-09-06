---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-19
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-20] `enableLiquidationAndRedeeming` pauses liquidations which can be problematic'
vuln_class: []
---

# [L-20] `enableLiquidationAndRedeeming` pauses liquidations which can be problematic

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`enableLiquidationAndRedeeming` is pausing both redemptions and liquidations

Those 2 operations have a very different purpose, with redemptions helping with the peg and acting as a pre-liquidation and liquidations being a necessary tool to make the system work

Due to this, liquidations should never be disabled unless a major bug was discovered

**Mitigation**

Separate `enableLiquidationAndRedeeming` to disable redemptions and liquidations separately
