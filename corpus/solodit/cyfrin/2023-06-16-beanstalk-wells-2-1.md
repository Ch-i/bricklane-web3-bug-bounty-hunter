---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Lack of validation for `A` in `GeoEmaAndCumSmaPump::constructor`
vuln_class: []
---

# Lack of validation for `A` in `GeoEmaAndCumSmaPump::constructor`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

**Description:** In the `GeoEmaAndCumSmaPump::constructor`, the EMA parameter ($\alpha$) `A` is initialized to `_A`. This parameter is supposed to be less than 1 otherwise `GeoEmaAndCumSmaPump::update` will revert due to underflow.

**Impact:** Given this initialization is done by the deployer on initialization, we evaluate the severity to LOW.

**Recommended Mitigation:** Require the initialization value `_A` to be less than `ABDKMathQuad.ONE`.

**Beanstalk:** Fixed in commit [e834f9f](https://github.com/BeanstalkFarms/Basin/commit/e834f9f6114815fbfef1a406cb0bb773449a6bc2).

**Cyfrin:** Acknowledged.
