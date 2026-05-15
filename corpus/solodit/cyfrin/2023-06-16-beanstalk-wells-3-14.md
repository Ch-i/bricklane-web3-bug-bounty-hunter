---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-14
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
title: Insufficient use of NatSpec and comments on complex code blocks
vuln_class: []
---

# Insufficient use of NatSpec and comments on complex code blocks

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

Many low-level functions, such as `WellDeployer::encodeAndBoreWell`, are missing NatSpec documentation. Additionally, many math-heavy contracts and libraries can only be easier to understand with NatSpec and supporting comments.

**Beanstalk:** Added natspec to `encodeAndBoreWell`. Fixed [here](https://github.com/BeanstalkFarms/Basin/pull/65).

**Cyfrin:** Acknowledged.
