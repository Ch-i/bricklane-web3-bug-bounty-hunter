---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: Redundant cast in contract TokenVesting.sol, at line 143 timestamp is being
  cast to uint256 although it is received as a parameter of type uin256.
vuln_class: []
---

# Redundant cast in contract TokenVesting.sol, at line 143 timestamp is being cast to uint256 although it is received as a parameter of type uin256.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Remove the cast at line 143.
