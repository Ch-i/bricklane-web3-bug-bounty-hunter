---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-1
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
title: Constant block time assumption could be invalidated, affecting calculation
  of `SeasonFacet::gm` incentives
vuln_class: []
---

# Constant block time assumption could be invalidated, affecting calculation of `SeasonFacet::gm` incentives

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The block time of Ethereum, despite having never been constant, always has a target time toward which blocks are added. On occasion, this value has changed. Initially, in PoW Ethereum, the block time target was approximately 13-14 seconds, but with the PoS Merge in 2022 this [changed](https://ycharts.com/indicators/ethereum_average_block_time) to 12 seconds. This means that any [assumption](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/C.sol#L28) of a constant average block time could be invalidated. Therefore, the blocks late [calculation](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L136-L141) within the call to [`SeasonFacet::incentivize`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L61) would be incorrect if, in future, the target block time changes, affecting the [expected Bean rewards](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/LibIncentive.sol#L65-L107).
