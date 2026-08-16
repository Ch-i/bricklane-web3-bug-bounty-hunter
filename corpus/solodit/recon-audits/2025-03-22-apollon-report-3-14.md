---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-14
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
title: '[L-15] `claimUnassignedAsset` `_percentage` can be more than 1e18'
vuln_class: []
---

# [L-15] `claimUnassignedAsset` `_percentage` can be more than 1e18

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/BorrowerOperations.sol#L614-L620

```solidity
  function claimUnassignedAssets(
    uint _percentage,
    address _upperHint,
    address _lowerHint,
    bytes[] memory _priceUpdateData
  ) external payable override {
    if (_percentage == 0) revert ZeroDebtChange();
```

Maybe abused for exploit, I haven't spent a lot of time on this, it's best to cap it to 1e18 to avoid any additional risk

**Mitigation** 

```solidity
if (_percentage > DECIMAL_PRECISION) revert Above100Pct();
```
