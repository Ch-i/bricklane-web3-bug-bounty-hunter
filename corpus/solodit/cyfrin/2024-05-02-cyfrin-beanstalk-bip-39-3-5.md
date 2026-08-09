---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Miscellaneous NatSpec and inline comment errors
vuln_class: []
---

# Miscellaneous NatSpec and inline comment errors

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

The following NatSpec errors were identified:
- [`UnripeFacet::balanceOfPenalizedUnderlying`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/barn/UnripeFacet.sol#L208-L214) NatSpec is incorrectly copied from [`UnripeFacet::balanceOfUnderlying`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/barn/UnripeFacet.sol#L194-L201) and should be modified for this particular function.
- The NatSpec of [`LibWell::getTwaReservesForWell`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/Well/LibWell.sol#L189) is incorrect. It states that this function returns the `USD / TKN` price stored in `{AppStorage.usdTokenPrice}`; however, this is actually the `TKN / USD` price and should be updated accordingly.
- A [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/sun/SeasonFacet/Weather.sol#L90) explaining the implementation of`Weather::updateTemperature` incorrectly references `uint32(-change)` where it should instead be `uint256(-change)`.
- A [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibCases.sol#L55) in `LibCases` explaining the behavior of the constants incorrectly states `Bean2maxLpGpPerBdv set to 10% of current value` when it should be 50% of the current value.
- A [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/init/InitBipNewSilo.sol#L77) in `InitBipNewSilo` has been changed to state the `stemStartSeason` is stored as a `uint32` when it is actually `uint16`.
- The NatSpec for the [`int8[32] cases`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/AppStorage.sol#L456) member of `AppStorage` is outdated and along with the [member itself](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/AppStorage.sol#L507) should be marked as deprecated in favor of `bytes32[144] casesV2`.
- There is a slight error in the case of [`TwaReserves`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/AppStorage.sol#L499) in the NatSpec of `AppStorage` which should instead be `twaReserves`.
- [`deprecated_beanEthPrice`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/AppStorage.sol#L564) does not currently exist in the NatSpec of `AppStorage`. It should be added along with an explanation of why this member is deprecated.
