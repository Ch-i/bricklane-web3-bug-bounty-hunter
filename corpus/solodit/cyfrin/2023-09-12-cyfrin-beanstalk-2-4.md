---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Missing reentrancy guard in `TokenFacet::transferToken`
vuln_class: []
---

# Missing reentrancy guard in `TokenFacet::transferToken`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Unlike most other external and potentially state-modifying functions in `TokenFacet`, [`TokenFacet::transferToken`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/farm/TokenFacet.sol#L56-L62) does not have the `nonReentrant` modifier applied. While we have been unable to identify a vector for exploit based on the current commit hash, it is recommended to add the modifier to this function to be in keeping with the rest of the code and prevent any potential future misuse.
