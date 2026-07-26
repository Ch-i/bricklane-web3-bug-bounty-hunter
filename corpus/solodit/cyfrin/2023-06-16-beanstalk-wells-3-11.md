---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-11
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Missing test coverage for a number of functions
vuln_class: []
---

# Missing test coverage for a number of functions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

Consider adding tests for `GeoEmaAndCumSmaPump::getSlotsOffset`, `GeoEmaAndCumSmaPump::getDeltaTimestamp`, and `_getImmutableArgsOffset` to increase test coverage and confidence that they are working as expected.

**Beanstalk:** Fixed [here](https://github.com/BeanstalkFarms/Basin/pull/67).

**Cyfrin:** Acknowledged.
