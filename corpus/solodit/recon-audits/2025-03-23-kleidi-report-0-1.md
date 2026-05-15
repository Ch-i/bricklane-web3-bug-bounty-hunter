---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-kleidi-report-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-kleidi-report
title: '[L-02] `Timelock` Permissionless `execute` could cause issues and out of order
  operations when multiple operations are ready'
vuln_class: []
---

# [L-02] `Timelock` Permissionless `execute` could cause issues and out of order operations when multiple operations are ready

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Kleidi_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Kleidi_Report.md)_

---

**Impact**

`execute` can be called by anyone

Meaning that once an operation is ready, it can be broadcasted by any caller

This also means that if more than one operation is ready at a specific time, the order of execution may be altered

This could be done for multiple reasons:
- Cause a revert
- Create MEV opportunities
- Cause a misconfiguration at the end of the sequence

**Sonne Example**

An extreme example is what happened with Sonne finance:
https://rekt.news/sonne-finance-rekt/
https://medium.com/@SonneFinance/post-mortem-sonne-finance-exploit-12f3daa82b06

They had queued the creation of a Compound Fork Market, the setting of 0% collateral factor, adding collateral and burning them as 3 separate operations, allowing the exploiter to only perform the creation of the market

**Realistic Example**
In the case of the Timelock, because certain operations such as `removeCalldataCheck` and `removeCalldataCheckDatahash` rely on an index, out of order operations may cause reverts or misconfiguration

**Mitigation**

It's important to document the risks of not using batch operations to end users

As long as end users batch their operations, no meaningful risk should be present
