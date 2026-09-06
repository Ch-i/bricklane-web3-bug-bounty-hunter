---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-0
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
title: '[L-01] `LiquidationsOperations` Comment around `_emitLiquidationSummaryEvent`
  is incorrect'
vuln_class: []
---

# [L-01] `LiquidationsOperations` Comment around `_emitLiquidationSummaryEvent` is incorrect

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

`_emitLiquidationSummaryEvent` has the following comment
https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/LiquidationOperations.sol#L447-L455

```solidity

  function _emitLiquidationSummaryEvent(LocalVariables_OuterLiquidationFunction memory vars) internal {
    TokenAmount[] memory liquidatedColl = new TokenAmount[](vars.priceCache.collPrices.length);
    for (uint i = 0; i < vars.priceCache.collPrices.length; i++) {
      liquidatedColl[i] = TokenAmount(
        vars.priceCache.collPrices[i].tokenAddress,
        vars.tokensToRedistribute[i].amount // works because of the initialisation of the array (first debts, then colls) /// @audit Wrong comment
      );
    }
```

The comment looks wrong since the array fills in collaterals first and then debts

**Mitigation**

Check the comments and fix them
