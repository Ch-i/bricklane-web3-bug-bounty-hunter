---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-2
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
title: Possible underflow when handling after-actions for token.
vuln_class: []
---

# Possible underflow when handling after-actions for token.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

When ATokens are minted, transferred, or burnt, 
ChefIncentivesController.handleActionAfter() is called, and it updates balances and total supplies in mappings 'userInfo` and `poolInfo`. 
However, during disqualification, the contract calls ChefIncentivesController.disqualifyUser() when the user's balance is set to 0 (by calling_handleActionAfter ForToken() where_balance = 0). 
However, ATokens are still present on the user's balance. When he tries to transfer or burn them, the contract calls handleActionAfter() and performs a subtraction from 0. That might cause an underflow, granting users an enormous balance and affecting the correctness of rewards distribution. 

**Recommendation**: 

Do not set userInfo[user].amount to Ø during disqualification in order to avoid underflows when user transfers or burns his tokens. 

**Post-audit**: 

Subtraction is validated now. Also since user's current amount is subtracted from total supply, it won't cause an underflow.
