---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Legacy Pipeline address defined in `DepotFacet`
vuln_class: []
---

# Legacy Pipeline address defined in `DepotFacet`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, `DepotFacet` references an old implementation of Pipeline with the todo comment that it should be updated:
```solidity
address private constant PIPELINE =
    0xb1bE0000bFdcDDc92A8290202830C4Ef689dCeaa; // TODO: Update with final address.
```
It is understood that this todo comment has been resolved in a more recent commit and should now appear as follows:
```diff
- address private constant PIPELINE = 0xb1bE0000bFdcDDc92A8290202830C4Ef689dCeaa; // TODO: Update with final address.
+ address private constant PIPELINE = 0xb1bE0000C6B3C62749b5F0c92480146452D15423;
```
