---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2021-05-06-shield-finance-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2021-05-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md
tags:
- firm:zokyo
- report:2021-05-06-shield-finance
title: Extra variable
vuln_class: []
---

# Extra variable

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2021-05-06-Shield Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2021-05-06-Shield%20Finance.md)_

---

Line, 95, _mint() function.
Since there is overloaded totalSupply() method, prefix “super.totalSupply()” can be omitted so
as the local variable. Require statement may be simplified to “getMaxTotalSupply() >=
(totalSupply() + amount)”. For now such statements are confusing and misleading,

**Recommendation**: 

simplify _mint() function.
