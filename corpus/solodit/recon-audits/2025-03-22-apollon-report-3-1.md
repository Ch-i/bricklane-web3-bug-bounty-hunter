---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-02] `LiquidationOperations` loop should `break` on last Trove'
vuln_class: []
---

# [L-02] `LiquidationOperations` loop should `break` on last Trove

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Apollon will not liquidate the last trove in `batchLiquidateTroves` 
However, the code is using a `continue` which means that the code will loop multiple times while performing no-ops

```solidity
     if (troveManager.getTroveOwnersCount() <= 1) continue; // don't liquidate if last trove
```

**Mitigation**

Change the code to

```solidity
      if (troveManager.getTroveOwnersCount() <= 1) break; // no more troves to liquidate
```
