---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-25
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Remove unused/unnecessary constants in `LibIncentive`
vuln_class: []
---

# Remove unused/unnecessary constants in `LibIncentive`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

`LibIncentive` currently defines a [`PERIOD`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibIncentive.sol#L23-L24) constant for the Uniswap Oracle lookback window, which is both unused and incorrect – this should be removed. This library also defines [`BASE_FEE_CONTRACT`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibIncentive.sol#L45-L46), which shadows a constant of the same name and value in `C.sol` – this can also be removed in favor of the [definition](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/C.sol#L75-L76) in `C.sol`.
