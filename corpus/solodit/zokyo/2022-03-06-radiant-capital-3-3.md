---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Same tokens can be added to eligible tokens array.
vuln_class: []
---

# Same tokens can be added to eligible tokens array.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

EligibilityDataProvider.sol: add Token(). 
The owner is able to set the same token as eligible multiple times. Thus the same token will be added to the array 'eligibleTokens multiple times. The issue is marked as info since it doesn't affect the contract, as array is not used in any of its logic. However, it might be crucial for other parts of the protocol that the array doesn't contain repeatable tokens, so it is recommended to restrict the same token to be added to the array multiple times. 

**Recommendation**:

Validate that 'token' is not already added to array of eligible tokens. 

**Post-audit**. 
Function was removed.
