---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-8
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
title: '[L-09] Up to (1e18 - 1) loss in interest paid due to rounding down'
vuln_class: []
---

# [L-09] Up to (1e18 - 1) loss in interest paid due to rounding down

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`stableInterest` in `_calculatePendingBorrowingInterest` rounds down the amount to be paid due to division before multiplication 

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/TroveManager.sol#L459-L462

```solidity
      stableInterest += /// Can find cheaper price to pay less, ultimately subject to "downward spiral" and other risks
        (((_priceFeed.getUSDValue(_priceCache, address(debtToken), debtTokenAmount) * borrowingInterestRate) /
          DECIMAL_PRECISION) * timePassed) /
        SECONDS_PER_YEAR;
```

There is no particular risk of overflow and the loss is up to `DECIMAL_PRECISION - 1`

**Mitigation**

Change the formula to:

```solidity
      stableInterest +=
        (((_priceFeed.getUSDValue(_priceCache, address(debtToken), debtTokenAmount) * borrowingInterestRate) * timePassed) / DECIMAL_PRECISION /
        SECONDS_PER_YEAR;
```
