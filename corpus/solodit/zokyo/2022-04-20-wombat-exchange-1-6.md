---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-6
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: In contract Pool.sol the IMasterWombat is declared, line 63, as variable and
  set in storage through the setMasterWombat at lines 202-205. It is then used in
  function deposit, at lines 446 and 447.
vuln_class: []
---

# In contract Pool.sol the IMasterWombat is declared, line 63, as variable and set in storage through the setMasterWombat at lines 202-205. It is then used in function deposit, at lines 446 and 447.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Consider declaring/storing only the address of the MasterWombat, as masterWombatAddress and use in-place interface initialization such as IMasterWombat(masterWombaAddress).someFunc(..) as this can reduce gas cost.
