---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-4-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Simplify modulo operations
vuln_class: []
---

# Simplify modulo operations

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

In `LibBytes::storeUint128` and `LibBytes::readUint128`, `reserves.lenth % 2 == 1` and `i % 2 == 1` can be simplified to `reserves.length & 1 == 1` and `i & 1 == 1`.

**Beanstalk:** Fixed in commit [9db714a](https://github.com/BeanstalkFarms/Basin/commits/9db714a35a8674852e4c9ac41e1b9e548e21b38f).

**Cyfrin:** Acknowledged.
