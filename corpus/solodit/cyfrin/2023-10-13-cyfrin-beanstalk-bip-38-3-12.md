---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-10-13-cyfrin-beanstalk-bip-38-3-12
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
title: Typo in comment within `LibSilo::_mow`
vuln_class: []
---

# Typo in comment within `LibSilo::_mow`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-10-13-cyfrin-beanstalk-bip-38.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-10-13-cyfrin-beanstalk-bip-38.md)_

---

The following [typo](https://github.com/BeanstalkFarms/Beanstalk/blob/12c608a22535e3a1fe379db1153185fe43851ea7/protocol/contracts/libraries/Silo/LibSilo.sol#L351-L352) in `LibSilo::_mow` should be corrected:

```diff
- //sop stuff only needs to be updated once per season
- //if it started raininga nd it's still raining, or there was a sop
+ // sop stuff only needs to be updated once per season
+ // if it started raining and it's still raining, or there was a sop
```

**Beanstalk Farms:** Fixed in commit [d27567c](https://github.com/BeanstalkFarms/Beanstalk/pull/655/commits/d27567c5f84bf07d604397f4d4549570ac9fb8c4).

**Cyfrin:** Acknowledged.
