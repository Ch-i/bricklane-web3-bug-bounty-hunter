---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-8
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
title: '`InitBipBasinIntegration` NatSpec title tag is inconsistent with the file/contract
  name'
vuln_class: []
---

# `InitBipBasinIntegration` NatSpec title tag is inconsistent with the file/contract name

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

The [title tag](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/beanstalk/init/InitBipBasinIntegration.sol#L17) of the `InitBipBasinIntegration` NatSpec is inconsistent with the file/contract name and should be updated to match.

**Beanstalk Farms:** Fixed in commit [c03f635](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/c03f635ef655eb80a2f6a270c41f19bcbd4a66ad).

**Cyfrin:** Acknowledged.
