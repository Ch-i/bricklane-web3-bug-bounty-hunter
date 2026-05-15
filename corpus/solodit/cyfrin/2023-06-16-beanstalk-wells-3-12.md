---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-12
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
title: Use `uint256` over `uint`
vuln_class: []
---

# Use `uint256` over `uint`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

`uint` is an alias for `uint256` and is not recommended for use. The variable size should be clarified, as this can cause issues when encoding data with selectors if the alias is mistakenly used within the signature string.

**Beanstalk:** Fixed in commit [7ca7d64](https://github.com/BeanstalkFarms/Basin/commits/7ca7d64866ee8235641c6cc4bb71df511d1f61a5).

**Cyfrin:** Acknowledged.
