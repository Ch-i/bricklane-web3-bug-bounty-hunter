---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-3
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
title: Potential DoS in `FertilizerFacet::getFertilizers` if enough Fertilizer is
  added
vuln_class: []
---

# Potential DoS in `FertilizerFacet::getFertilizers` if enough Fertilizer is added

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

It is possible that [`FertilizerFacet::getFertilizers`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/barn/FertilizerFacet.sol#L172-L192) can be susceptible to DoS if enough Fertilizer NFTs are minted, given that it attempts to query all the nodes of a linked list in two separate while loops. This function is not used anywhere else within the protocol and appears for UI/UX purposes only, but any potential third-party integrations should consider this issue carefully.
