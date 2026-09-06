---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-0
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
title: Non-standard storage packing
vuln_class: []
---

# Non-standard storage packing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

Per the [Solidity docs](https://docs.soliditylang.org/en/v0.8.17/internals/layout_in_storage.html), the first item in a packed storage slot is stored lower-order aligned; however, [manual packing](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/libraries/LibBytes.sol#L37) in `LibBytes` does not follow this convention. Modify the `storeUint128` function to store the first packed value at the lower-order aligned position.

**Beanstalk:** Fixed in commit [5e61420](https://github.com/BeanstalkFarms/Basin/pull/71/commits/5e614205a49f1388c36b2a02ce38cf0df317dfde).

**Cyfrin:** Acknowledged.
