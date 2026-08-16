---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-21
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
title: '`LibUniswapOracle::PERIOD` comment should be resolved'
vuln_class: []
---

# `LibUniswapOracle::PERIOD` comment should be resolved

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

There is a [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Oracle/LibUniswapOracle.sol#L21) in `LibUniswapOracle` that suggests the [`PERIOD`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Oracle/LibUniswapOracle.sol#L22) constant may be incorrect. It is understood that this value is actually already correct, so the todo comment should be resolved and all references to a 30-minute lookback period in the Beanstalk whitepaper should be updated.
