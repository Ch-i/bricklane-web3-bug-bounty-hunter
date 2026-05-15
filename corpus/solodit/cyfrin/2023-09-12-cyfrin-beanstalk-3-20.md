---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-20
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Unused legacy function `LibTokenSilo::calculateStalkFromStemAndBdv` can be
  removed
vuln_class: []
---

# Unused legacy function `LibTokenSilo::calculateStalkFromStemAndBdv` can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

As [stated](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/ConvertFacet.sol#L205-L207) in `ConvertFacet::_depositTokensForConvert`, the legacy function [`LibTokenSilo::calculateStalkFromStemAndBdv`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibTokenSilo.sol#L416-L428) is no longer used and so can be removed. If it is desired to keep this function visible for reference, then it is recommended to comment it out.
