---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-06] `TroveManager``_calcBorrowingRate` always returns `borrowingFeeFloor`'
vuln_class: []
---

# [M-06] `TroveManager``_calcBorrowingRate` always returns `borrowingFeeFloor`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`_calcBorrowingRate` is using `min(X + Y, X)` meaning it will always return `X` in this case `borrowingFeeFloor`

**Mitigation**

Change 
```solidity
  function _calcBorrowingRate(uint _stableCoinBaseRate) internal view returns (uint) {
    return LiquityMath._min(borrowingFeeFloor + _stableCoinBaseRate, borrowingFeeFloor);
  }
```

To
```solidity
  function _calcBorrowingRate(uint _stableCoinBaseRate) internal view returns (uint) {
    return LiquityMath._min(borrowingFeeFloor + _stableCoinBaseRate, 1e18);
  }
```
