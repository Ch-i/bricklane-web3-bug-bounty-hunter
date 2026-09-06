---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-14-impossible-finance-1-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-06-14T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md
tags:
- firm:zokyo
- report:2021-06-14-impossible-finance
title: Solidity version update.
vuln_class: []
---

# Solidity version update.

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-06-14-Impossible Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-14-Impossible%20Finance.md)_

---

**Description**

The solidity version should be updated. Throughout the project (including interfaces).
Issue is classified as Medium, because it is included to the list of standard smart contracts’
vulnerabilities.

**Recommendation**:

You need to update the solidity version to the latest one - at least to 0.6.12, though 0.7.6 will
be the best option. This will help to get rid of bugs in the older versions.
