---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-16-beanstalk-wells-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md
tags:
- firm:cyfrin
- report:2023-06-16-beanstalk-wells
title: Remove experimental ABIEncoderV2 pragma
vuln_class: []
---

# Remove experimental ABIEncoderV2 pragma

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-16-Beanstalk wells.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-16-Beanstalk%20wells.md)_

---

ABIEncoderV2 is enabled by default in Solidity 0.8, so [two](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/interfaces/IWellFunction.sol#L4) [instances](https://github.com/BeanstalkFarms/Wells/blob/e5441fc78f0fd4b77a898812d0fd22cb43a0af55/src/interfaces/pumps/IPump.sol#L4) can be removed.

**Beanstalk:** All instances of ABIEncoderV2 pragma have been removed. Fixed in commit [3416a2d](https://github.com/BeanstalkFarms/Basin/commit/3416a2d33876102158ab98a03f409903fe504278).

**Cyfrin:** Acknowledged.
