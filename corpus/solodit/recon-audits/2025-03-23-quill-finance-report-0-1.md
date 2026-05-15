---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-0-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[M-02] Must accrue `stabilityPoolYieldSplit` before changing it'
vuln_class: []
---

# [M-02] Must accrue `stabilityPoolYieldSplit` before changing it

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

Changing the yield can change the results from `calcPendingSPYield`

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/ActivePool.sol#L150-L153

```solidity
    function calcPendingSPYield() external view returns (uint256) {
        return calcPendingAggInterest() * stabilityPoolYieldSplit / DECIMAL_PRECISION;
    }

```

This means that the estimated value could change

Based on integrations this can cause a repricing of a wrapped SP Token (staked Quill)

**Mitigation**

Mitigation is straightforward, just `mintAggInterest` before updating the value

**Mitigation Status**

Fixed: https://github.com/subvisual/quill/pull/381
