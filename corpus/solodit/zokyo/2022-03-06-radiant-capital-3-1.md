---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Lack of events.
vuln_class: []
---

# Lack of events.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

In order to track the historical changes of essential storage variables, it is recommended to emit events in setters on every change of variable. Thus the following setter function should emit an event. 
1. AutoCompounder.sol: addReward BaseTokens(), setRoutes(). 
2. Disqualifier.sol, EligibilityDataProvider.sol, MiddleFee Distribution.sol, Leverager.sol, RadiantOFT.sol, StargateBorrow.sol: all functions which start with "set". 

**Recommendation**: 

Emit events in setter functions.
