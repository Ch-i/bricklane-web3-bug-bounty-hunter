---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: EIP-1967 second pre-image best practice
vuln_class: []
---

# EIP-1967 second pre-image best practice

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

When calculating custom [EIP-1967](https://eips.ethereum.org/EIPS/eip-1967) storage slots, as in [Well.sol::RESERVES_STORAGE_SLOT](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/Well.sol#L25), it is [best practice](https://ethereum-magicians.org/t/eip-1967-standard-proxy-storage-slots/3185?u=frangio) to add an offset of `-1` to the hashed value to further reduce the possibility of a second pre-image attack.

**Beanstalk:** Fixed in commit [dc0fe45](https://github.com/BeanstalkFarms/Basin/commit/dc0fe45ae0b85bc230093acc8b35939cbc8f1844).

**Cyfrin:** Acknowledged.
