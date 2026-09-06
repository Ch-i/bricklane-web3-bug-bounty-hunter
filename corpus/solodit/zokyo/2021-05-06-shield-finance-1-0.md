---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-06-shield-finance-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2021-05-06T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md
tags:
- firm:zokyo
- report:2021-05-06-shield-finance
title: Missing mint method
vuln_class: []
---

# Missing mint method

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2021-05-06-Shield Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md)_

---

**Description**

Line 95, _mint() function overloading
Token’s initializer already provides mint for the full maximum supply (line 48, mint for
getMaxTotalSupply()). Though the token can enable burn functionality, so more place for
minting appears. Though, overloaded _mint() function is called from nowhere but from the
initializer, which is called only once. Looks like either public mint() function is absent, or
overload _mint() method is unnecessary.

**Recommendation**:

Clarify the minting logic and the necessity of _mint() and mint() methods.
