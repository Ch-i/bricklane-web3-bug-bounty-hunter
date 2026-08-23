---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Redundant condition in `LibSilo::_mow` can be removed
vuln_class: []
---

# Redundant condition in `LibSilo::_mow` can be removed

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

There is a [line](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L355) within `LibSilo::_mow` which performs some validation on the last update for a given account before handling Flood logic. The account's last update must be at least equal to the season when it started "raining" for it to be eligible for Season of Plenty (sop) rewards. There is also additional validation that the last update is less than or equal to the current season, which will, of course, always be the case given that it is [not possible](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L372) to update an account beyond the current season. Therefore, this condition can be removed as below:

```diff
- if (lastUpdate <= s.season.rainStart && lastUpdate <= s.season.current) {
+ if (lastUpdate <= s.season.rainStart) {
```
