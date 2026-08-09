---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-4
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
title: Unused imports and errors
vuln_class: []
---

# Unused imports and errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

In `LibMath`:
- OpenZeppelin SafeMath is imported but not used
- `PRBMath_MulDiv_Overflow` error is declared but never used

**Beanstalk:** Fixed [here](https://github.com/BeanstalkFarms/Basin/pull/65).

**Cyfrin:** Acknowledged.
