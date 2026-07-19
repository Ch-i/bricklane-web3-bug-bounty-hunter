---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Use globally available Solidity variables in `C.sol`
vuln_class: []
---

# Use globally available Solidity variables in `C.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

When specifying units of time in Solidity, literal numbers can be used with the suffixes `seconds`, `minutes`, `hours`, `days` and `weeks`. In the `C.sol` constants library, the following is recommended:
```diff
- uint256 private constant CURRENT_SEASON_PERIOD = 3600;
+ uint256 private constant CURRENT_SEASON_PERIOD = 1 hours;
```
