---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[M-03] `RedemptionOperations` allows redemption against stale prices'
vuln_class: []
---

# [M-03] `RedemptionOperations` allows redemption against stale prices

_Section severity (from Solodit section header): Medium_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The code for `_calculateTroveRedemption` doesn't validate that collaterals nor debts prices are not stale

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/RedemptionOperations.sol#L231-L259

```solidity
  function _calculateTroveRedemption(
    PriceCache memory _priceCache,
    address _borrower,
    uint _redeemMaxAmount,
    bool _includePendingRewards
  ) internal view returns (SingleRedemptionVariables memory vars) {
    address stableCoinAddress = address(tokenManager.getStableCoin());

    // stable coin debt should always exists because of the gas comp
    TokenAmount[] memory troveDebt = _includePendingRewards
      ? troveManager.getTroveRepayableDebts(_priceCache, _borrower, true) // with pending rewards
      : troveManager.getTroveDebt(_borrower); // without pending rewards
    if (troveDebt.length == 0) revert InvalidRedemptionHint();
    for (uint i = 0; i < troveDebt.length; i++) {
      TokenAmount memory debtEntry = troveDebt[i];

      if (debtEntry.tokenAddress == stableCoinAddress) vars.stableCoinEntry = debtEntry;
      vars.troveDebtInUSD += priceFeed.getUSDValue(_priceCache, debtEntry.tokenAddress, debtEntry.amount);
    }

    vars.collLots = _includePendingRewards
      ? troveManager.getTroveWithdrawableColls(_borrower)
      : troveManager.getTroveColl(_borrower);
    for (uint i = 0; i < vars.collLots.length; i++) {
      uint p = priceFeed.getUSDValue(_priceCache, vars.collLots[i].tokenAddress, vars.collLots[i].amount);
      vars.troveCollInUSD += p;
      if (!tokenManager.isDebtToken(vars.collLots[i].tokenAddress)) vars.redeemableTroveCollInUSD += p;
    } /// @audit can change the ratio of a trove to have mostly `isDebtToken` debt | How does this relate to collateral?

```

This opens up to arbitrage opportunities where the pyth price may be higher for a certain collateral, while the fallback oracle price is lower, allowing the caller to receive more collateral than what would be the fair market price

**Mitigation**

Rethink oracle price staleness checks to prevent arbitrages
