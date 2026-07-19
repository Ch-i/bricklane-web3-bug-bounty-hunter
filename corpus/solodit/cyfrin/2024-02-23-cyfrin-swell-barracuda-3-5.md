---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-02-23-cyfrin-swell-barracuda-3-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-02-23T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md
tags:
- firm:cyfrin
- report:2024-02-23-cyfrin-swell-barracuda
title: Refactor `RepricingOracle::handleReprice`, `_assertRepricingSnapshotValidity`
  and `_repricingPeriodDeltas`
vuln_class: []
---

# Refactor `RepricingOracle::handleReprice`, `_assertRepricingSnapshotValidity` and `_repricingPeriodDeltas`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-02-23-cyfrin-swell-barracuda.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-02-23-cyfrin-swell-barracuda.md)_

---

**Description:** In `RepricingOracle::_assertRepricingSnapshotValidity` and `_repricingPeriodDeltas` there is a lot of logic around whether to use the old snapshot or not, based around if `upgradeableRepriceSnapshot.meta.blockNumber == 0`.

If the idea is that the first time repricing occurs after the upgrade the execution path is `useOldSnapshot = true` but after that every time it will be `useOldSnapshot = false`, then it may make more sense to create functions just for that first execution which will only run once, then have functions for all the normal cases which come afterwards. This would avoid the extra gas costs and also simplify the code for all the future normal cases after the first-time-call special case.

Gas costs can also be reduced by having `handleReprice` load the snapshot struct, cache `upgradeableRepriceSnapshot.meta.blockNumber`, calculate `useOldSnapshot` once then pass these in as inputs to `_assertRepricingSnapshotValidity` and `_repricingPeriodDeltas` eg:

```solidity

  function handleReprice(
    UpgradeableRepriceSnapshot calldata _snapshot
  ) internal {
    // only call getSnapshotStruct() once
    UpgradeableRepriceSnapshot
      storage upgradeableRepriceSnapshot = getSnapshotStruct();

    // only calculate these once and pass them as required
    uint256 ursMetaBlockNumber = upgradeableRepriceSnapshot.meta.blockNumber;
    bool useOldSnapshot = ursMetaBlockNumber == 0;

    // validation
    _assertRepricingSnapshotValidity(_snapshot, ursMetaBlockNumber, useOldSnapshot);

    _repricingPeriodDeltas(
          reserveAssets,
          _snapshot.state,
          _snapshot.withdrawState,
          upgradeableRepriceSnapshot,
          useOldSnapshot
        );

    // delete the call to getSnapshotStruct() near the end of handleReprice()
```


**Swell:** Acknowledged. Will be addressed in a future upgrade when the old snapshot is no longer relevant. Swell will continue to pay the excess gas costs in the meantime.
