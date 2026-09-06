---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-24
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
title: Legacy code in `LibPRBMath` should be removed
vuln_class: []
---

# Legacy code in `LibPRBMath` should be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The commented versions of the [`SCALE_LPOTD`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPRBMath.sol#L24) and [`SCALE_INVERSE`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPRBMath.sol#L28) constants in `LibPRBMath` are taken from the original [PRBMath library](https://github.com/PaulRBerg/prb-math/blob/e33a042e4d1673fe9b333830b75c4765ccf3f5f2/contracts/PRBMath.sol#L113-L118) and are intended to work with unsigned 60.18-decimal fixed-point numbers. It is understood that the values of the [uncommented versions](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPRBMath.sol#L37-L42) of these constants were derived by the original author for modifications required by Beanstalk. These modifications are no longer used, and so, along with [`LibPRBMath::powu`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPRBMath.sol#L44-L57), [`LibPRBMath::logBase2`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPRBMath.sol#L33-L66) and [`LibPRBMath::mulDivFixedPoint`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibPRBMath.sol#L59C14-L96) should be removed.
