---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-05-02-cyfrin-beanstalk-bip-39-3-2
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
title: Outdated Seed Gauge System documentation in PR and inline comments
vuln_class: []
---

# Outdated Seed Gauge System documentation in PR and inline comments

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-05-02-cyfrin-beanstalk-bip-39.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-05-02-cyfrin-beanstalk-bip-39.md)_

---

There are multiple instances in both the PR and inline comments where documentation of the Seed Gauge System is outdated. For example:
- `LibWhitelist::updateGaugeForToken` does not allow the gauge points to be changed. This is contrary to the comment in [`WhitelistFacet::updateGaugeForToken`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/beanstalk/silo/WhitelistFacet.sol#L172).
- The behavior of [`LibGauge::getBeanToMaxLpGpPerBdvRatioScaled`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L316-L329) is incorrectly documented as the reverse of its actual behavior, which is `f(0) = MIN_BEAN_MAX_LPGP_RATIO` and `f(100e18) = MAX_BEAN_MAX_LPGP_RATIO`.
- Gauge Points are not normalized to `100e18`, as stated in the PR.
- The [`MIN_BEAN_MAX_LP_GP_PER_BDV_RATIO`](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L32) constant is actually `50e18`, not `25e18` as stated in the PR.
- `gpPerBdv` and `beanToMaxLpGpPerBdvRatio` both have 18 decimal precision, but there are [multiple](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L153) [comments](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L210) which [incorrectly](https://github.com/BeanstalkFarms/Beanstalk/blob/dfb418d185cd93eef08168ccaffe9de86bc1f062/protocol/contracts/libraries/LibGauge.sol#L215) state that these variables have 6 decimal precision.
