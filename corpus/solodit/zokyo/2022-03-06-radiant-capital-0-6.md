---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Transfer without enough token on contract balance.
vuln_class: []
---

# Transfer without enough token on contract balance.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Leverager: loop() 
The function will revert with isBorrow parameter = true since it cannot transfer fee without any tokens on balance. Also it seems like it is charging funds twice: before the for() cycle and in it. 

**Recommendation**:

Transfer fee when a contract has enough tokens on balance.
