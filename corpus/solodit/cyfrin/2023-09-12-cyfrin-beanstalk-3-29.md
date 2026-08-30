---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-09-12-cyfrin-beanstalk-3-29
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-09-12T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md
tags:
- firm:cyfrin
- report:2023-09-12-cyfrin-beanstalk
title: Shadowed `Prices` struct declaration should be resolved
vuln_class: []
---

# Shadowed `Prices` struct declaration should be resolved

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-09-12-cyfrin-beanstalk.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-09-12-cyfrin-beanstalk.md)_

---

Both `P.sol` and `BeanstalkPrice` declare a `Prices` struct of similar form. The version currently residing in `P.sol` should be modified as follows in favor of that in `BeanstalkPrice` which can then be subsequently be removed:

```diff
    struct Prices {
-       address pool;
-       address[] tokens;
        uint256 price;
        uint256 liquidity;
        int deltaB;
        P.Pool[] ps;
    }
```
