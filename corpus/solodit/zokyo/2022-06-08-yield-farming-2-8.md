---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-06-08-yield-farming-2-8
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2022-06-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md
tags:
- firm:zokyo
- report:2022-06-08-yield-farming
title: In contract UnifarmCohort, all the revert messages form the require functions
  are very short and hard to understand, we understand the reason for this was the
  gas optimization but this is not necessary, the strings in solidity are defined
  o
vuln_class: []
---

# In contract UnifarmCohort, all the revert messages form the require functions are very short and hard to understand, we understand the reason for this was the gas optimization but this is not necessary, the strings in solidity are defined on 32 bytes, so even if your string message hase only 2 characters in it, it will still take 32 bytes, so our recommendation would be to make the messages more clear and to take in consideration to not make them any longer then 32 bytes, if you can make them explicit and with a length of 32 bytes it will take as many gas as this short messages are taking right now.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-06-08-Yield Farming.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-06-08-Yield%20Farming.md)_

---

**Recommendation**:

Make the messages more explicative but no longer then 32 bytes because they are already
defined on 32 bytes, so there is no added benefit to make them shorter then 32 bytes,
prioritize clarity and explanations. (this was informational so skipping it)
