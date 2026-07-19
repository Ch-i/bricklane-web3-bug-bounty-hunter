---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-5
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
title: '[L-06] Riskiest Trove can be made to pay compound interest cheaply'
vuln_class: []
---

# [L-06] Riskiest Trove can be made to pay compound interest cheaply

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

Apollon charges simple interest on Trove Accrual

In general Troves can only be accrued by their owners during state-changing operations


```solidity
    for (uint i = 0; i < _iterations.length; i++) {
      RedeemIteration memory iteration = _iterations[i];
      checkValidRedemptionHint(vars.priceCache, iteration.trove);
      troveManager.applyPendingRewards(iteration.trove, vars.priceCache); /// @audit The Hint may be wrong NOW, the CR may be underwater now
      SingleRedemptionVariables memory troveRedemption = _calculateTroveRedemption( /// TODO: KEY
        vars.priceCache,
        iteration.trove,
        _stableCoinAmount - vars.totalRedeemedStable,
        false // without pending rewards, because they got applied above
      );

      // resulting CR differs from the expected CR, we bail in that case, because all following iterations will consume too much gas by searching for a updated hints
      // allowing 1% deviation, because of time based borrowing interests
      if (troveRedemption.resultingCR > iteration.expectedCR) {
        if ((troveRedemption.resultingCR * DECIMAL_PRECISION) / iteration.expectedCR > 1.01e18) break; /// @audit Risk of overflow
      } else {
        if ((iteration.expectedCR * DECIMAL_PRECISION) / troveRedemption.resultingCR > 1.01e18) break;
      }
```

However, the riskiest trove can be made to accrue by redeeming a very small amount of debt (e.g. 1 wei)

**Mitigation**

Either document this risk, or enforce a minimum redemption size
