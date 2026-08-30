---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-7
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Ternary operator in `Sun::rewardToHarvestable` can be simplified
vuln_class: []
---

# Ternary operator in `Sun::rewardToHarvestable` can be simplified

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

In [`Sun::rewardToHarvestable`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Sun.sol#L162-L172), the `newHarvestable` variable is [reassigned](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Sun.sol#L168-L170) to `notHarvestable` if it exceeds this value, essentially acting as a cap to prevent the case where the Harvestable index exceeds the Pod index when the reward amount is sufficiently large to cause all outstanding Pods in the Pod Line to become Harvestable. If this is not the case, such that there will remain Pods in the Pod Line that are not Harvestable, reassignment is made by the ternary operator to the existing `newHarvestable` value. This branch is not necessary and can be removed:

```diff
    newHarvestable = amount.div(HARVEST_DENOMINATOR);
-   newHarvestable = newHarvestable > notHarvestable
-       ? notHarvestable
-       : newHarvestable;
+   if (newHarvestable > notHarvestable) {
+       newHarvestable = notHarvestable;
+   }
```
