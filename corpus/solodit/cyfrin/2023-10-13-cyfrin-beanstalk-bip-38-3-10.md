---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-10
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-10-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md
tags:
- firm:cyfrin
- report:2023-10-13-cyfrin-beanstalk-bip-38
title: Unsafe cast in `WellPrice::getDeltaB`
vuln_class: []
---

# Unsafe cast in `WellPrice::getDeltaB`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

While not likely to overflow, there is an [unsafe cast](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/ecosystem/price/WellPrice.sol#L97) in `WellPrice::getDeltaB` which could be replaced with a safe cast.

**Beanstalk Farms:** Fixed in commit [ff742a6](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/ff742a6f5b0b166df988a2422e475d314b948fc9).
