---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-18
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
title: '`Sun::setSoilAbovePeg` considers intervals for `caseId` larger than intended'
vuln_class: []
---

# `Sun::setSoilAbovePeg` considers intervals for `caseId` larger than intended

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

As is [commented](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Sun.sol#L219) in the NatSpec of [`Sun::setSoilAbovePeg`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Sun.sol#L226-L234), Beanstalk wants to gauge demand for Soil _when above peg_. As such, based on the implementation of [`InitBip13`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/init/InitBip13.sol#L18-L30), the following modifications should be made:

```diff
-   if (caseId >= 24) {
+   if (caseId >= 28) {
         newSoil = newSoil.mul(SOIL_COEFFICIENT_HIGH).div(C.PRECISION); // high podrate
-   } else if (caseId < 8) {
+   } else if (4 <= caseId < 8) {
         newSoil = newSoil.mul(SOIL_COEFFICIENT_LOW).div(C.PRECISION); // low podrate
    }
```

This does not affect the Soil mechanism because the `caseId` [passed](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L58) to [`Sun::stepSun`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Sun.sol#L66-L83) when called in [`SeasonFacet::gm`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/SeasonFacet.sol#L47-L62) has already been correctly calculated from within [`Weather::stepWeather`](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/sun/SeasonFacet/Weather.sol#L100-L172); however, it is recommended to modify the logic so that its implementation strictly conforms to its intention.
