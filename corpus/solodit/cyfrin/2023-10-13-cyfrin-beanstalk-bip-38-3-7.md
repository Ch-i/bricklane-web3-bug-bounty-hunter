---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Continued reference to "Seeds" in `InitBipBasinIntegration::init` is confusing
vuln_class: []
---

# Continued reference to "Seeds" in `InitBipBasinIntegration::init` is confusing

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

With the deprecation of the "Seeds" terminology, [continued reference](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/init/InitBipBasinIntegration.sol#L31-L33) is confusing and all instances should be updated to instead refer to the earned Stalk per BDV per Season.

**Beanstalk Farms:** Updated names in commit [ba1d42b](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/ba1d42bc9159881143c5f23ab03a7ba8078bd4b0).
