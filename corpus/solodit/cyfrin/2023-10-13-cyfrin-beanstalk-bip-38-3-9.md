---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Conditional block in `WellPrice::getConstantProductWell` can be removed
vuln_class: []
---

# Conditional block in `WellPrice::getConstantProductWell` can be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

The [else block](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/ecosystem/price/WellPrice.sol#L64-L67) in `WellPrice::getConstantProductWell`, which handles the case when it is not possible to determine a price for Bean, is not necessary and can be removed as the default value of the `pool.price` is already zero.

**Beanstalk Farms:** Removed in commit [8aae31d](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/8aae31d683aeec50ccbc17985701b46223cc0a1d).

**Cyfrin:** Acknowledged.
