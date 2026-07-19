---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-4-8
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Unnecessary reassignment of `deltaB` to its default value in `LibCurveMinting::check`
vuln_class: []
---

# Unnecessary reassignment of `deltaB` to its default value in `LibCurveMinting::check`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

When returning the time-weighted average `deltaB` in the BEAN/3CRV Metapool since the last Sunrise, `LibCurveMinting::check` unnecessarily reassigns `deltaB` to the default `int256` value (zero) if the Curve oracle is not initialized. Given that `deltaB` is declared in the function signature return value and is nowhere else used before this reassignment, this branch can be removed:

```diff
    if (s.co.initialized) {
        (deltaB, ) = twaDeltaB();
-   } else {
-       deltaB = 0;
    }
```
