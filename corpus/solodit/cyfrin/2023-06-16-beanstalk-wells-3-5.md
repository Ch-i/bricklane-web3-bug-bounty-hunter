---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-5
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Inconsistency in LibMath comments
vuln_class: []
---

# Inconsistency in LibMath comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

There is inconsistent use of `x` in comments and `a` in code within the `nthRoot` and `sqrt` [functions](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/libraries/LibMath.sol#L41-L138) of `LibMath`.

**Beanstalk:** Fixed [here](https://github.com/BeanstalkFarms/Basin/pull/65).

**Cyfrin:** Acknowledged.
