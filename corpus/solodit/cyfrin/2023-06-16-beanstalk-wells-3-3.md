---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Inconsistent use of decimal/hex notation in inline assembly
vuln_class: []
---

# Inconsistent use of decimal/hex notation in inline assembly

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

For readability and to prevent errors when working with inline assembly, decimal notation should be used for integer constants and hex notation for memory offsets.

**Beanstalk:** All new code written for Basin uses decimal notation. Decimal notation has been selected for all new code as it is more readable.

Some external libraries use hex notation (Ex. `ABDKMathQuad.sol`. It was decided that it is best to leave these libraries as is instead of modifying them to prevent complication.

**Cyfrin:** Acknowledged.
