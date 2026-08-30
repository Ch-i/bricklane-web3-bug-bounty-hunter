---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-0-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[M-03] `CCR == SCR` can cause unintended shutdown when the protocol has only
  one Trove per Branch'
vuln_class: []
---

# [M-03] `CCR == SCR` can cause unintended shutdown when the protocol has only one Trove per Branch

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

The deployment scripts for Quill looks as follows:

https://github.com/subvisual/quill/blob/23e53123a16b12614d25bfb715e17dd41bcebbdd/contracts/scripts/DeployQuillLocal.s.sol#L38-L42

```solidity
        TroveManagerParams[] memory troveManagerParamsArray = new TroveManagerParams[](4);
        troveManagerParamsArray[0] = TroveManagerParams(150e16, 110e16, 110e16, 5e16, 10e16, 500e18, 72e16, _1pct / 2); // WETH
        troveManagerParamsArray[1] = TroveManagerParams(150e16, 120e16, 110e16, 5e16, 10e16, 500e18, 72e16, _1pct / 2); // wstETH
        troveManagerParamsArray[2] = TroveManagerParams(150e16, 120e16, 110e16, 5e16, 10e16, 500e18, 72e16, _1pct / 2); // weETH
        troveManagerParamsArray[3] = TroveManagerParams(150e16, 120e16, 110e16, 5e16, 10e16, 500e18, 72e16, _1pct / 2); // SCROLL
```

The MCR and SCR are matching, this means that for Branches that have one Trove, that trove could cause a shutdown of the branch as soon as the Trove is liquidatable

**Mitigation**

Either set the SCR to a lower amount

Or perform the following as part of your deployment:
- Open a trove on each branch
- Redeem it down to 0 debt
- Keep it open for each branch

This will make it so that no single borrower could cause a branch to shutdown
