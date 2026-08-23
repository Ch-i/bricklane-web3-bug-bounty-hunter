---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-stakedao-onlyboost-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md
tags:
- firm:zachobront
- report:2023-11-01-stakedao-onlyboost
title: '[M-05] Deployment script mismatches gauges and reward distributors'
vuln_class: []
---

# [M-05] Deployment script mismatches gauges and reward distributors

_Section severity (from Solodit section header): Medium_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-StakeDAO-Onlyboost.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-StakeDAO-Onlyboost.md)_

---

In Deployment.s.sol, a list of gauges (Curve) and reward distributors (StakeDAO) are provided to migrate.

The gauge list is 162 elements long, but the reward distributor list is only 160 elements long, missing the corresponding reward distributors to the final two gauges.

The match between these two lists is crucial, as funds will be migrated and permissions granted accordingly.

**Recommendation**

Beyond adding the two missing reward distributors, I recommend adding checks to the deployment script to ensure the two lists are equal length and the addresses at each index are intended to correspond with each other:
```diff
+ require(rewardDistributors.length == gauges.length);
  for (uint256 i = 0; i < rewardDistributors.length; i++) {
+     IStrategy oldStrategy = IStrategy(locker.governance());
+     require(oldStrategy.multigauges(gauges[i]) == rewardDistributors[i]);
      ...
  }
```

**Review**

Fixed as recommended in commit [315fc02e6b9b97698b1b24f2e853151513590707](https://github.com/stake-dao/only-boost/commit/315fc02e6b9b97698b1b24f2e853151513590707).
