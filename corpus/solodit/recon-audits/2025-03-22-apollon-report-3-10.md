---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-11] Stablecoin interest being lower than jTokens seems inconsistent + Tokens
  with different volatilities pay the same fee'
vuln_class: []
---

# [L-11] Stablecoin interest being lower than jTokens seems inconsistent + Tokens with different volatilities pay the same fee

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Generally speaking jAssets will be more volatile and riskier than a stablecoin that denominates them

The logic for `getBorrowingRate` charges more for stableCoins than for jAssets

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/TroveManager.sol#L898-L901

```solidity
  function getBorrowingRate(bool isStableCoin) public view override returns (uint) {
    if (!isStableCoin) return borrowingFeeFloor;
    return _calcBorrowingRate(stableCoinBaseRate);
  }
```

It's also worth noting that all assets pay the same interest rate which means that they don't pay based on risk

**Mitigation**

Consider whether you should charge different fees for different assets so that the system is compensated for the additional risk it's taking
