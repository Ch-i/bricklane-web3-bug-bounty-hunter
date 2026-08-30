---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-1
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Lack of Validation for Loan Funding Status
vuln_class: []
---

# Lack of Validation for Loan Funding Status

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**: 

The withdrawFunds function does not validate whether the loan has been fully funded before allowing the seller to withdraw funds. This could lead to a situation where a seller attempts to withdraw funds before the loan is adequately capitalized.

**Scenario**:

A loan is created, but for some reason, the funding process is delayed or incomplete.
The seller, without realizing the loan isn't fully funded, calls the withdrawFunds function.
Since there’s no validation check, the function might proceed with transferring funds, leading to an unexpected contract state or even financial discrepancies.

**Impact**: 

This can lead to an inconsistent state where the loan is not properly funded but funds are withdrawn. This could also potentially open up avenues for abuse, where a seller could try to withdraw funds from a partially funded loan.

**Recommendation**: 

Add a validation check in the withdrawFunds function to ensure that the loan's funding status is confirmed before allowing any withdrawal. This can be achieved by checking if the loan’s startDate is set (indicating the loan is funded).

**Client comment**: 

This is confirmed to be an issue: if the Pool Admin has not invoked LoanManager::fundLoan and the seller has already triggered LoanManager::withdrawFunds, the receivable will be transferred from the seller to the LoanManager contract. However, no asset tokens will be transferred since the loan's drawableFunds is not a non-zero amount. This prevents the user from withdrawing the funds again, making the receivable and the corresponding loan unusable.
