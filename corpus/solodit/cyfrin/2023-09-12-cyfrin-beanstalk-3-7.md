---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-7
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Incorrect contract addresses in `C.sol`
vuln_class: []
---

# Incorrect contract addresses in `C.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

There are [two address constants](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/C.sol#L81-L82) in `C.sol` which have been added as part of the BEAN/ETH Well integration. Currently, `BEANSTALK_PUMP` references the crv3crypto address, defined by the [`TRI_CRYPTO`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/C.sol#L62) constant above, while `BEAN_ETH_WELL` references an address with no code. It is understood that these addresses were chosen arbitrarily for the purpose of testing until the final versions of these contracts are deployed. It is also understood that these addresses have been updated in a more recent commit with no impact on test output despite the collision with another existing address within the system.
