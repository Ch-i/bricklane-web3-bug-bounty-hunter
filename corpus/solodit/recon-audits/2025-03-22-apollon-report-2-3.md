---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-04] `LiquidationOperations.batchLiquidateTroves` redistributes bad debt
  and collateral after all operations, meaning it will allow skipping bad debt redistribution
  during liquidations'
vuln_class: []
---

# [M-04] `LiquidationOperations.batchLiquidateTroves` redistributes bad debt and collateral after all operations, meaning it will allow skipping bad debt redistribution during liquidations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The code for `batchLiquidateTroves` is as follows:

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/LiquidationOperations.sol#L106-L137

```solidity
  function batchLiquidateTroves(address[] memory _troveArray, bytes[] memory _priceUpdateData) public payable override {
    if (!troveManager.enableLiquidationAndRedeeming()) revert LiquidationDisabled(); /// @audit MUST be separate
    if (_troveArray.length == 0) revert EmptyArray();

    LocalVariables_OuterLiquidationFunction memory vars;

    // update prices and build price cache
    priceFeed.updatePythPrices{ value: msg.value }(_priceUpdateData); /// @audit custom update on oracle prices, doesn't guarantee everything will be valid
    vars.priceCache = priceFeed.buildPriceCache();

    (vars.isRecoveryMode, vars.TCR, vars.entireSystemCollInUSD, vars.entireSystemDebtInUSD) = storagePool
      .checkRecoveryMode(vars.priceCache);
    vars.remainingStabilities = stabilityPoolManager.getRemainingStability(vars.priceCache);
    _initializeEmptyTokensToRedistribute(vars); // all set to 0 (nothing to redistribute)

    bool atLeastOneTroveLiquidated = false;
    for (uint i = 0; i < _troveArray.length; i++) {
      address trove = _troveArray[i];
      if (!troveManager.isTroveActive(trove)) continue; // Skip non-active troves | // @audit TODO: Are these ones with 0 debt?
      if (troveManager.getTroveOwnersCount() <= 1) continue; // don't liquidate if last trove /// @audit Break?

      bool liquidated = _executeTroveLiquidation(vars, trove); /// @audit Out of order Sorting based on Risk, to maximize profit
      if (liquidated && !atLeastOneTroveLiquidated) atLeastOneTroveLiquidated = true;
    }
    if (!atLeastOneTroveLiquidated) revert NoLiquidatableTrove();

    // move tokens into the stability pools
    stabilityPoolManager.offset(vars.priceCache, vars.remainingStabilities); /// @audit Redistribute, but pay from reserve?

    // and redistribute the rest (which could not be handled by the stability pool)
    troveManager.redistributeDebtAndColl(vars.priceCache, vars.tokensToRedistribute); /// @audit But computed here ??

```

Where in the loop, liquidations are done on Troves for which their Debt and Coll is computed on pre-liquidation storage values:
https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/LiquidationOperations.sol#L186-L192

```solidity
    (
      vars.troveAmountsIncludingRewards,
      vars.IMCR,
      vars.troveCollInUSD,
      vars.troveDebtInUSD,
      vars.troveDebtInUSDWithoutGasCompensation
    ) = troveManager.getEntireDebtAndColl(outerVars.priceCache, trove);
```

Meaning that redistributions of Debt and Coll are skipped while doing the batch liquidation

This will result in a higher premium to liquidators than intended, and a higher loss to CollStakers when the redistribution happens

**Mitigation**

This is an issue with how the math for liquidation is computed, because it applies only to very specific edge cases, it may be best to let end users know as the fix would require having in-memory accounting of debt redistribution, which will increase complexity
