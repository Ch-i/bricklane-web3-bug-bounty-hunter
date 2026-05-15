---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-4
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: The gracePeriod_ parameter in the requestLoan function of the LoanManager can
  be set indefinitely allowing the attacker to protect themselves from defaults if
  funded
vuln_class: []
---

# The gracePeriod_ parameter in the requestLoan function of the LoanManager can be set indefinitely allowing the attacker to protect themselves from defaults if funded

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Location**: LoanManager.sol#requestLoan

**Description**: 

The requestLoan function of the LoanManager contract allows a buyer when requesting a loan to specify a grace period for the loan. This is seen as a “warning” period for which the borrower will have to return their loan to a healthy state or else their position will be put into a defaulted state by the pool configurator admin. There exists a condition in the triggerDefault function of the loan manager which will check if the loan is past the supplied grace period. 

Because this value can be set to an indefinite value (ie. a date that is excessively far into the future), this can prevent the admin from triggering a default on the loan if repayments aren’t made.

**Recommendation**

Consider allowing the pool configurator admin to set a maximum threshold after a loan due date for which grace periods can be set to prevent overly extensive grace periods. It’s recommended that there are additional validations made on the grace period when requesting a loan. 

**Client comment**: 

 This scenario is similar to the one mentioned in this issue's comments. While the buyer can set arbitrary parameters in the LoanManager::requestLoan function, the request may still be rejected by the Pool Admin.
Pool Admin use a multi-signature wallet, such as Safe, instead of a single wallet. This will enhance security and ensure that loan approvals are more robust, reducing the risk of arbitrary or bad loans being approved by a single party..
