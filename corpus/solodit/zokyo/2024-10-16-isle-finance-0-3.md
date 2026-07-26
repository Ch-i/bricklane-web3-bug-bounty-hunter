---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Interest rates can be arbitrary which can allow the loan requester to set them
  to zero bypassing interest and late interest rates if funded
vuln_class: []
---

# Interest rates can be arbitrary which can allow the loan requester to set them to zero bypassing interest and late interest rates if funded

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged

**Location**: LoanManager.sol#requestLoan

**Description**: 

The LoanManager allows a buyer to request a loan from the pool using the requestLoan function. The buyer can pass various parameters to the function such as the receivable asset, the receivables token id, grace period, principal requested and the interest rates as an array. The interestRate (as defined by the 0th index of the rates_ array) and the lateInterestPremiumRate (as defined by the 1st index of the rates_ array) can effectively be arbitrary. This can allow the buyer to specify these as zero in order to bypass interest rates.

**Recommendation**

It’s recommended that the contract admin sets these interest rates using setters within the contract. The interest rates array should be validated against these state variables.

**Client comment**: 

Pool Admin use a multi-signature wallet, such as Safe, instead of a single wallet. This will enhance security and ensure that loan approvals are more robust, reducing the risk of arbitrary or bad loans being approved by a single party..
