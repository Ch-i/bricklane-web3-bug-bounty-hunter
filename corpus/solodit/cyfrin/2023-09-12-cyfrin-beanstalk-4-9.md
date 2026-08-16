---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-9
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: 'Execution of `LibLegacyTokenSilo:: balanceOfGrownStalkUpToStemsDeployment`
  can end earlier when `lastUpdate == stemStartSeason`'
vuln_class: []
---

# Execution of `LibLegacyTokenSilo:: balanceOfGrownStalkUpToStemsDeployment` can end earlier when `lastUpdate == stemStartSeason`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, `LibLegacyTokenSilo:: balanceOfGrownStalkUpToStemsDeployment` [returns zero](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibLegacyTokenSilo.sol#L188) if the last update season is greater than the Stems deployment season, given this implies the account has already been credited the grown Stalk it was owed. This optimization can also be made when the last update season is equal to the Stems deployment season, as the [multiplication](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibLegacyTokenSilo.sol#L220) of the account's Seeds by a season difference of zero yields zero outstanding grown Stalk.

```diff
- if (lastUpdate > stemStartSeason) return 0;
+ if (lastUpdate >= stemStartSeason) return 0;
```
