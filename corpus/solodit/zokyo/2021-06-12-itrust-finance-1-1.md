---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-06-12-itrust-finance-1-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2021-06-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md
tags:
- firm:zokyo
- report:2021-06-12-itrust-finance
title: Solidity version update
vuln_class: []
---

# Solidity version update

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-06-12-iTrust Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-06-12-iTrust%20Finance.md)_

---

**Description**

The solidity version should be updated. Throughout the project (including interfaces).
Issue is classified as Medium, because it is included to the list of standard smart contracts’
vulnerabilities. Currently used version (0.7.5) is not the last in the line, which contradicts the
standard checklist.

**Recommendation**: 

You need to update the solidity version to the latest one in the branch -
0.7.6.
