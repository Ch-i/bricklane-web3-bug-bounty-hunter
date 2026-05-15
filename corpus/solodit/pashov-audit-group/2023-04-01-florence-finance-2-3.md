---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[M-04] The `apr` and `fundingFee` percentage values are not constrained'
vuln_class: []
---

# [M-04] The `apr` and `fundingFee` percentage values are not constrained

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
High, as this can result in the contract being in a state of DoS or in 0 rewards for users

**Likelihood:**
Low, as it requires a malicious or a compromised owner, or a big mistake on the owner side

**Description**

Neither the `setApr` nor the `setFundingFee` methods have input validations, checking if the percentage value arguments are too big or too small. A malicious/compromised owner, or one that does a "fat-finger", can input a huge number as those methods' argument, which will result in a state of DoS for the contract. Also the values of 0 or 100 (percentage) are valid as well, but shouldn't be - they will result in either 0 rewards for users or high fees (100% fees are not possible because of the slippage check in `approveFundingAttempt`).

**Recommendations**

Add a min and max value checks in both the `setApr` and `setFundingFee` methods in `LoanVault`.
