---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-4-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Cache recapitalized amount to prevent extra storage read
vuln_class: []
---

# Cache recapitalized amount to prevent extra storage read

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

`LibFertilizer::remainingRecapitalization` should cache `s.recapitalized` then use the cached stack variable in [L166-167](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibFertilizer.sol#L166-L167) to prevent reading the same value a second twice from storage.
