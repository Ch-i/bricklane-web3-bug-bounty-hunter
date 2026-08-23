---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-11-01-wrappedelon-1-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md
tags:
- firm:pashov-audit-group
- report:2023-11-01-wrappedelon
title: '[L-03] Protocol is using a vulnerable library version'
vuln_class: []
---

# [L-03] Protocol is using a vulnerable library version

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-11-01-WrappedElon.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-11-01-WrappedElon.md)_

---

In `package.json` file in the repository we can see this:

```javascript
"@openzeppelin/contracts": "^4.7.3",
```

This version contains multiple vulnerabilities as you can see [here](https://github.com/OpenZeppelin/openzeppelin-contracts/security/advisories). While the problems are not present in the current codebase, it is strongly advised to upgrade the version to v4.9.5 which has fixes for all of the vulnerabilities found so far after v4.7.3.
