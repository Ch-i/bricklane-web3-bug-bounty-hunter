---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Use underscore prefix for internal functions
vuln_class: []
---

# Use underscore prefix for internal functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

For functions such as `getSlotForAddress`, it is more readable to have this function be named `_getSlotForAddress` so readers know it is an internal function. A similarly opinionated recommendation is to use `s_` for storage variables and `i_` for immutable variables.

**Beanstalk:** Decided to add the `_` prefix to internal functions, but not the `s_` or `i_` prefix. Fixed in commit [86c471f](https://github.com/BeanstalkFarms/Basin/pull/76/commits/86c471f9767ccea4bfa49a34fd6344ae77e74f24).

**Cyfrin:** Acknowledged.
