---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-9
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Incorrect comment in `FieldFacet::_sow` NatSpec
vuln_class: []
---

# Incorrect comment in `FieldFacet::_sow` NatSpec

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

The [comment](https://github.com/BeanstalkFarms/Beanstalk/blob/c7a20e56a0a6659c09314a877b440198eff0cd81/protocol/contracts/beanstalk/field/FieldFacet.sol#L131) explaining how `FundraiserFacet::fund` bypasses soil updates in the `FieldFacet::_sow` NatSpec incorrectly references `LibDibbler::sowWithMin` when this should in fact be `LibDibbler::sowNoSoil`, as below:

```diff
    /**
     * @dev Burn Beans, Sows at the provided `_morningTemperature`, increments the total
     * number of `beanSown`.
     *
     * NOTE: {FundraiserFacet} also burns Beans but bypasses the soil mechanism
-    * by calling {LibDibbler.sowWithMin} which bypasses updates to `s.f.beanSown`
+    * by calling {LibDibbler.sowNoSoil} which bypasses updates to `s.f.beanSown`
     * and `s.f.soil`. This is by design, as the Fundraiser has no impact on peg
     * maintenance and thus should not change the supply of Soil.
     */
```
