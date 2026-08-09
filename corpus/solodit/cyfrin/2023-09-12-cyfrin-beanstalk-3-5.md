---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Duplicated update logic to an account's `lastUpdate` in `LibSilo::_mow` can
  be simplified
vuln_class: []
---

# Duplicated update logic to an account's `lastUpdate` in `LibSilo::_mow` can be simplified

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, the update to an account's `lastUpdate` in `LibSilo::_mow` occurs twice – both [after handling Flood logic](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L362) and then again at the [end of the function](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L372). It appears that this second instance was added as mitigation against a [different issue](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L370-L371); however, it has the implication that the first instance is no longer needed as the second will always be reached in the case of successful execution, and none of the remaining logic depends on the value of the account's `lastUpdate`.

Additionally, the [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L360-L361) preceding the first update is irrelevant here as the case it describes is [handled by `LibSilo::__mow`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L391-L393) – if the last stem equals the current stem tip then execution ends, and no additional grown stalk can be claimed.
