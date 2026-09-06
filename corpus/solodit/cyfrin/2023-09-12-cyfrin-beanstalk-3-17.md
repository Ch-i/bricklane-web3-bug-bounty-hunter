---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-17
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Incorrect comment in `Oracle::totalDeltaB` NatSpec
vuln_class: []
---

# Incorrect comment in `Oracle::totalDeltaB` NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Currently, `Oracle::totalDeltaB` [states](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Oracle.sol#L23) that this function returns the current shortage/excess of Beans (`deltaB`) in the BEAN/3CRV Curve liquidity pool; however, it [actually returns the sum](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Oracle.sol#L26-L28) of `deltaB` across both the Curve pool and BEAN/ETH Well and so the comment should be updated to reflect this.
