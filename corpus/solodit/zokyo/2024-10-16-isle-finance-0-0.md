---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Inconsistent Loan Impairment Handling Due to Missing Reset of isImpaired Flag
vuln_class: []
---

# Inconsistent Loan Impairment Handling Due to Missing Reset of isImpaired Flag

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**: 

The removeLoanImpairment function in the LoanManager contract fails to reset the isImpaired flag to false after removing a loan's impairment. As a result, the loan remains incorrectly marked as impaired, leading to inconsistencies in how the loan is managed by the contract. This can cause incorrect calculations of unrealized losses and improper handling of loan defaults.

**Scenario**:

A loan is impaired by calling the impairLoan function, which correctly sets the isImpaired flag to true.
Later, the removeLoanImpairment function is called to remove the impairment. However, the function does not reset the isImpaired flag to false.
Despite the loan no longer being impaired, subsequent operations (such as triggerDefault) continue to treat the loan as impaired, leading to incorrect behavior and calculations.
For example, the unrealized losses calculated in PoolConfigurator::triggerDefault may be overstated because the loan is still incorrectly considered impaired.

**Recommendation**: 

Update the removeLoanImpairment function to include a line that resets the isImpaired flag to false after successfully removing the impairment. This ensures that the loan's state is correctly managed and that subsequent operations handle the loan as expected
