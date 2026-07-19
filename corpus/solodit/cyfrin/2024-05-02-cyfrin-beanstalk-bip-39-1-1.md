---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2024-05-02T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md
tags:
- firm:cyfrin
- report:2024-05-02-cyfrin-beanstalk-bip-39
title: Gauge point updates should be made considering the time-weighted average deposited
  LP BDV rather than instantaneous at the time of Sunrise
vuln_class: []
---

# Gauge point updates should be made considering the time-weighted average deposited LP BDV rather than instantaneous at the time of Sunrise

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

**Description:** Prior to the introduction of the Seed Gauge System, the Grown Stalk per BDV for whitelisted assets was static and could only be changed via governance. The Seed Gauge System now allows Beanstalk to target an amount of Grown Stalk per BDV that should be issued per Season, with Gauge Points being introduced to determine how the Grown Stalk issued that Season should be distributed between whitelisted LP tokens.

Gauge Points are updated every Season, when `LibGauge::stepGauge` is called within `SeasonFacet::gm`. This Gauge Point update is currently performed by [considering the instantaneous total deposited LP BDV](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L115-L122) at the time of the `gm` call. However, this value can be subject to manipulation so the Seed Gauge System should instead use a time-weighted average deposited LP BDV over the previous Season duration.

**Impact:** Given the Gauge Points for a given whitelisted LP can only increase/decrease by one point per Season, and the Bean to max LP GP per BDV ratio is capped at 100%, the incentive to perform this attack is relatively low. However, a large deposit immediately before the Sunrise call, and withdrawal immediately after, could nonetheless result in manipulation meaning the Seed Gauge system does not work as intended.

**Recommended Mitigation:** Consider calculating time-weighted average deposited LP BDVs over the previous Season duration rather than using an instantaneous value. The BDV to include in the calculation at each block should be the one at the end of the previous block to avoid in-block manipulation. These values should be stored and the update should be triggered whenever a function is called which modifies the total deposited BDV in any way.
