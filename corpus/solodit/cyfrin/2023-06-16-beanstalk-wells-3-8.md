---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Poorly descriptive variable and function names in `GeoEmaAndCumSmaPump` are
  difficult to read
vuln_class: []
---

# Poorly descriptive variable and function names in `GeoEmaAndCumSmaPump` are difficult to read

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

For example, in `update`:
* `b` could be renamed `returnedReserves`.
* `aN` could be renamed `alphaN` or `alphaRaisedToTheDeltaTimeStamp`.

Additionally, `A`/`_A` could be renamed `ALPHA`, and `readN` could be renamed `readNumberOfReserves`.

**Beanstalk:** Fixed in commit [3bf0080](https://github.com/BeanstalkFarms/Basin/pull/78/commits/3bf0080f7597eb3dfc276ece6207f4f98dcc3db3).

* Rename `Reserves` struct to `PumpState`.
* Rename `b` to `pumpState`.
* Rename `readN` to `readNumberOfReserves`.
* Rename `n` to `numberOfReserves`.
* Rename `_A` to `_alpha`.
* Rename `A` to `ALPHA`.
* Rename `aN` to `alphaN`.

**Cyfrin:** Acknowledged.
