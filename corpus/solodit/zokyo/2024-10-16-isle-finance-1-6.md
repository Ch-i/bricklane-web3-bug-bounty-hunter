---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: Imprudent Withdrawal of Funds from Impaired Loans
vuln_class: []
---

# Imprudent Withdrawal of Funds from Impaired Loans

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Informational

**Status**: Acknowledged 

**Description**: 

In the current implementation of the LoanManager::withdrawFunds function, there is no explicit check to prevent withdrawals from impaired loans. As a result, even if a loan has been impaired, which indicates a high-risk or non-performing status, the seller can still withdraw the drawable funds associated with that loan. This loophole undermines the purpose of impairing loans and can lead to significant financial losses.

**Scenario**:

A loan is created and funded, with the seller having drawable funds.
Due to some unforeseen circumstances, the loan is impaired, indicating that the loan is at high risk or is no longer performing as expected.
Despite the impairment, the seller calls the withdrawFunds function, withdrawing the funds associated with the impaired loan.
The platform or the pool suffers financial losses because the impaired loan was allowed to proceed with fund withdrawal, contrary to standard risk management practices.

**Impact**: 

Allowing withdrawals from impaired loans can lead to significant financial losses, undermining the integrity of the lending platform. The impairment status should act as a safeguard to prevent any further financial transactions on high-risk loans until the issues are resolved.

**Recommendation**: 

Add Impairment Check:
Modify the withdrawFunds function to include a check that prevents withdrawals if the loan is impaired

**Client Comment** : 
In our protocol design, roles are separated to ensure that the seller can always withdraw funds, while any impairment primarily affects the lender. The issue description states that LoanManager::withdrawFunds prevents potential financial losses, but this is not entirely accurate. The Pool Admin can call LoanManager::fundLoan, transferring funds from the pool contract to the LoanManager contract. As a result, restricting LoanManager::withdrawFunds does not mitigate the impairment scenario
