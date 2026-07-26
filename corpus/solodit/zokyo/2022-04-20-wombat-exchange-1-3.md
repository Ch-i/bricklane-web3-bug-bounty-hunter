---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-04-20-wombat-exchange-1-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2022-04-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md
tags:
- firm:zokyo
- report:2022-04-20-wombat-exchange
title: 'In contract TokenVesting.sol in function _vestingSchedule at lines 156-175
  there is no default return path for the function. Also, the condition at line 165
  will always be  true as the parameter timestamp is passed from release function
  as '
vuln_class: []
---

# In contract TokenVesting.sol in function _vestingSchedule at lines 156-175 there is no default return path for the function. Also, the condition at line 165 will always be  true as the parameter timestamp is passed from release function as block.timestamp.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-04-20-Wombat Exchange.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-04-20-Wombat%20Exchange.md)_

---

**Recommendation**: Consider changing the order of conditions by calling _calculateInterval only once and then have the isUnlocked check and update the _unlockIntervalsCount. Attached below is a snippet of how this can be refactored.


 ![image](https://github.com/user-attachments/assets/ae0a95fd-72bc-4eaf-bb65-f8a13b06f827)
