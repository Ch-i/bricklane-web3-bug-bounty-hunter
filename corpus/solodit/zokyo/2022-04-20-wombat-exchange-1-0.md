---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: In contract Pool.sol, in function “setFeeTo”, error message that appears when
  “feeTo” is zero address is not the expected one.
vuln_class: []
---

# In contract Pool.sol, in function “setFeeTo”, error message that appears when “feeTo” is zero address is not the expected one.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Use “_checkAddress” function instead of checking through an if, at line 238.
