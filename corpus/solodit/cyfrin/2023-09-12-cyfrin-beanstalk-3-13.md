---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-13
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
title: '`LibSilo::_removeDepositsFromAccount` events may be emitted with additional
  `amounts` elements when called from `EnrootFacet::enrootDeposits` with `amounts.length
  > stems.length`'
vuln_class: []
---

# `LibSilo::_removeDepositsFromAccount` events may be emitted with additional `amounts` elements when called from `EnrootFacet::enrootDeposits` with `amounts.length > stems.length`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

For the purpose of gas efficiency, `EnrootFacet::enrootDeposits` does not validate that its `stems` and `amounts` array arguments are of the same length. [Looping](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/EnrootFacet.sol#L138) over the `stems` array, any additional `amounts` elements would remain unused and in the case of `amounts.length < stems.length` this would result in an index out-of-bounds error. The same is true of the [call](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/silo/EnrootFacet.sol#L64-L69) to [`LibSilo::_removeDepositsFromAccount`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L577) which makes use of these arguments; however, in the case where `amounts` contains additional elements then these will be emitted [`LibSilo::TransferBatch`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L616) and [`LibSilo::RemoveDeposits`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/libraries/Silo/LibSilo.sol#L617) events which may be undesirable.
