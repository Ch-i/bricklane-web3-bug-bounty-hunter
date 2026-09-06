---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-23-quill-finance-report-1-4
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-03-23T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md
tags:
- firm:recon-audits
- report:2025-03-23-quill-finance-report
title: '[L-05] Governance Raising the CCR could be used to prevent people from borrowing
  by griefer'
vuln_class: []
---

# [L-05] Governance Raising the CCR could be used to prevent people from borrowing by griefer

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-23-Quill_Finance_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-23-Quill_Finance_Report.md)_

---

**Impact**

This is partially mitigated by
`_requireNoBorrowingUnlessNewTCRisAboveCCR(_troveChange.debtIncrease, newTCR);`

https://github.com/subvisual/quill/blob/d4a5dcc168dfc315eef6a4c9c465a36c86ca0ddc/contracts/src/TroveManager.sol#L261-L280

```solidity
    function setNewBranchConfiguration(
        uint256 _scr,
        uint256 _mcr,
        uint256 _ccr,
        uint256 _newLiquidationPenaltySP,
        uint256 _newLiquidationPenaltyRedistribution
    ) external {
        _requireCallerIsCollateralRegistry();
        _requireValidConfig(_ccr, _mcr, _scr, _newLiquidationPenaltySP, _newLiquidationPenaltyRedistribution);

        SCR = _scr;
        MCR = _mcr;
        CCR = _ccr;
        liquidationPenaltySP = _newLiquidationPenaltySP;
        liquidationPenaltyRedistribution = _newLiquidationPenaltyRedistribution;

        emit BranchConfigurationUpdated(
            _scr, _mcr, _ccr, _newLiquidationPenaltySP, _newLiquidationPenaltyRedistribution
        );
    }
```

**Mitigation**

Perform multiple checks in your governance process to prevent griefing if possible
