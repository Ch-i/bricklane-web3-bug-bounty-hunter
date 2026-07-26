---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-11
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Typo in `FertilizerFacet::getMintFertilizerOut` NatSpec
vuln_class: []
---

# Typo in `FertilizerFacet::getMintFertilizerOut` NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

The NatSpec of [`FertilizerFacet::getMintFertilizerOut`](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/barn/FertilizerFacet.sol#L108) currently refers to Fertilizer as `Fertilize` which should be corrected.

**Beanstalk Farms:** Fixed in commit [373c094](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/373c0948cce9730446111a943a4fd96dabd90025).

**Cyfrin:** Acknowledged.
