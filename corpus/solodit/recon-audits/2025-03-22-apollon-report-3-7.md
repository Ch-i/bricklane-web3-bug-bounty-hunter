---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-7
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
title: '[L-08] Liquidation Logic will not work on all troves when the system is underwater'
vuln_class: []
---

# [L-08] Liquidation Logic will not work on all troves when the system is underwater

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`batchLiquidateTroves` allows for out of order liquidations

In the edge case of all troves being underwater, meaning all troves should be liquidated, the following check will allow liquidations only starting from the riskiest trove

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/LiquidationOperations.sol#L196-L197

```solidity
    if (vars.ICR > outerVars.TCR) return false; /// @audit Looks wrong in edge cases

```

This is more of a gotcha than a real risk as having all Troves underwater is a failure scenario

**Mitigation**

The check could be refactored to ensure that if all Troves are underwater, the vast majority of the debt can still be liquidated
