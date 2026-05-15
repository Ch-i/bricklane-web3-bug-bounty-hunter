---
affected_contracts: []
derives_from: []
id: solodit-recon-audits-2025-03-22-apollon-report-3-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-03-22T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md
tags:
- firm:recon-audits
- report:2025-03-22-apollon-report
title: '[L-10] Bad Debt Redistribution can be avoided by removing collaterals'
vuln_class: []
---

# [L-10] Bad Debt Redistribution can be avoided by removing collaterals

_Section severity (from Solodit section header): Low_  
_Audit firm: Recon Audits_  
_Source report: [2025-03-22-Apollon_Report.md](https://github.com/solodit/solodit_content/blob/main/reports/Recon%20Audits/2025-03-22-Apollon_Report.md)_

---

**Impact**

The logic for `redistributeDebtAndColl` is as follows

https://github.com/blkswnStudio/ap/blob/8fab2b32b4f55efd92819bd1d0da9bed4b339e87/packages/contracts/contracts/TroveManager.sol#L310-L337

```solidity
  function redistributeDebtAndColl(PriceCache memory _priceCache, CAmount[] memory toRedistribute) external override {
    _requireCallerIsBorrowerOpsOrRedemptionOpsOrLiquidationOps();

    // sum up all coll usd values
    uint totalRedistributedCollInUsd;
    uint[] memory collCacheInUSD = new uint[](toRedistribute.length);
    for (uint i = 0; i < toRedistribute.length; i++) {
      CAmount memory collEntry = toRedistribute[i];
      if (!collEntry.isColl || collEntry.amount == 0) continue; /// collCacheInUSD[i] = collInUSD || 0 when skipped

      uint collInUSD = priceFeed.getUSDValue(_priceCache, collEntry.tokenAddress, collEntry.amount);
      collCacheInUSD[i] = collInUSD;
      totalRedistributedCollInUsd += collInUSD;
    }

    // iterate over the coll entries and process the debt relative to the coll percentage
    uint[] memory debtsToDefaultPool = new uint[](toRedistribute.length);
    for (uint i = 0; i < toRedistribute.length; i++) { /// @audit technically same loop as above, since it skips the same entries
      CAmount memory collEntry = toRedistribute[i];
      if (!collEntry.isColl || collEntry.amount == 0) continue;

      // patch the liquidated coll tokens
      uint collTotalStake = totalStakes[collEntry.tokenAddress]; /// @audit Can you have 0 stakes by having a Trove that didn't redistribute?
      PoolType targetPool;
      if (collTotalStake == 0) {
        // the last trove with that coll type was liquidated/close, moving the assets into a claimable (unassigned) pool
        targetPool = PoolType.Unassigned;
      } else {
```

Specifically when `collTotalStake` is zero a redistribution for that collateral is skipped, sending debt and collateral to the `Unassigned` pool

This means that some users will be able to skip the redistribution by re-organizing their collateral before performing liquidations

It's worth noting that liquidations present a race condition against this behaviour meaning this can theoretically happen, but in some scenarios, an attacker won't be able to pull it off unless they are performing the liquidations as well
