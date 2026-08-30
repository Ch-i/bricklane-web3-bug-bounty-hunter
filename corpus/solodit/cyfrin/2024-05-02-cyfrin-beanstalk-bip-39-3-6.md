---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-6
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Time-weighted average reserves should be read from the Beanstalk Pump in `LibWell`
  using a `try/catch` block
vuln_class: []
---

# Time-weighted average reserves should be read from the Beanstalk Pump in `LibWell` using a `try/catch` block

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

There are instances in [`LibWell::getTwaReservesFromBeanstalkPump`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Well/LibWell.sol#L242) and [`LibWell::getTwaLiquidityFromBeanstalkPump`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Well/LibWell.sol#L262) where the time-weighted average reserves are read directly from the Beanstalk Pump. Unlike the implementation in [`LibWellMinting::twaDeltaB`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Minting/LibWellMinting.sol#L160), these functions do not wrap the call in a `try/catch` block. This should not affect the Beanstalk Sunrise mechanism as the execution of `LibWell::getTwaReservesFromStorageOrBeanstalkPump` will not reach the [invocation](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Well/LibWell.sol#L228) of `LibWell::getTwaReservesFromBeanstalkPump`, since here the reserves are already set in storage, but consider handling Pump failure gracefully so that [`LibEvaluate::calcLPToSupplyRatio`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibEvaluate.sol#L222) and [`SeasonGettersFacet::getBeanEthTwaUsdLiquidity`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonGettersFacet.sol#L227-L232) (which is also used in [`SeasonGettersFacet::getTotalUsdLiquidity`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonGettersFacet.sol#L238-L240)) do not revert if there is an issue.
