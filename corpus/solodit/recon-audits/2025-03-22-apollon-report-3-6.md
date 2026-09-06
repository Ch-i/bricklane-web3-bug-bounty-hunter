---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-6
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
title: '[L-07] Redemptions that redeem close to 100% of the Trove Debt may revert
  when the hint is inaccurate'
vuln_class: []
---

# [L-07] Redemptions that redeem close to 100% of the Trove Debt may revert when the hint is inaccurate

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

After a redemption, this comparison is performed:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L123-L129

```solidity
      // resulting CR differs from the expected CR, we bail in that case, because all following iterations will consume too much gas by searching for a updated hints
      // allowing 1% deviation, because of time based borrowing interests
      if (troveRedemption.resultingCR > iteration.expectedCR) {
        if ((troveRedemption.resultingCR * DECIMAL_PRECISION) / iteration.expectedCR > 1.01e18) break; /// @audit Risk of overflow
      } else {
        if ((iteration.expectedCR * DECIMAL_PRECISION) / troveRedemption.resultingCR > 1.01e18) break;
      }
```

Whenever expectedCR or resultingCR are greater than type(uint256).max / 1e18 the multiplication will overflow, causing a revert

This may be used to grief other people, or can happen naturally due to slight changes in prices, or other redemptions

**Mitigation**

It may be best to use a smaller factor such as `100` as to reduce the likelyhood of an overflow
