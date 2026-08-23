---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-16
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Miscellaneous comments on `TokenSilo` NatSpec and legacy references
vuln_class: []
---

# Miscellaneous comments on `TokenSilo` NatSpec and legacy references

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Beanstalk previously implemented a withdrawal queue that was later replaced by a per-Season vesting period. The `TokenSilo` contract NatSpec currently still [references](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/SiloFacet/TokenSilo.sol#L20-L21) this legacy withdrawal system but should be updated to reflect the current implementation pertaining to the removal of Stem-based deposits.

Additionally, references to "Crates" and [`crateBdv`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/SiloFacet/TokenSilo.sol#L348) should be removed and updated to `bdvRemoved` respectively. The [NatSpec of `TokenSilo::tokenSettings`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/SiloFacet/TokenSilo.sol#L430-L446) is missing references to [`milestoneStem`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L403-L406) and [`encodeType`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L408-L411) which are also present in the `SiloSettings` storage struct. Consider reordering this comment to accurately reflect the order of elements in the [declaration](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/AppStorage.sol#L373) within `AppStorage.sol`.
