---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-2
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: In contract TokenVesting.sol, redundant initialization of IERC20(vestedToken)
  at line 133 inside safeTransfer. The vestedToken is already an IERC20 initialized
  in the constructor.
vuln_class: []
---

# In contract TokenVesting.sol, redundant initialization of IERC20(vestedToken) at line 133 inside safeTransfer. The vestedToken is already an IERC20 initialized in the constructor.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Remove the initialization of IERC20 inside the safeTransfer call. Also, might consider dropping the initialization in the constructor and storing only the address and initializing only inside the safeTransfer call at line 133, as it reduces gas.
