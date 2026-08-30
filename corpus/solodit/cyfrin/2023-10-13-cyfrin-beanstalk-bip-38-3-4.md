---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Logic in `LibFertilizer::push` related to (deprecated) intermediate addition
  of Fertilizer to FIFO list should be removed
vuln_class: []
---

# Logic in `LibFertilizer::push` related to (deprecated) intermediate addition of Fertilizer to FIFO list should be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

Intermediate addition to the FIFO list was formerly allowed only by the Beanstalk DAO, but this functionality has since been deprecated in the current upgrade with the removal of `FertilizerFacet::addFertilizerOwner`. Consequently, the [corresponding logic](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/libraries/LibFertilizer.sol#L139-L147) in `LibFertilizer::push` should be removed as this now represents unreachable code.

**Beanstalk Farms:** the `push(...)` function is still used internally [here](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/libraries/LibFertilizer.sol#L60).

The highlighted segment is not used reachable anymore, but in the case where the humidity is changed for some reason, it could again be reached. For this reason, the decision was made to leave it in.

**Cyfrin:** Acknowledged.
