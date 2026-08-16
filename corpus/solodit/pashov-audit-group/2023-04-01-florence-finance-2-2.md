---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-2-2
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[M-03] User exit/claim methods should not have a `whenNotPaused` modifier'
vuln_class: []
---

# [M-03] User exit/claim methods should not have a `whenNotPaused` modifier

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
High, as user funds can be left stuck in the contract

**Likelihood:**
Low, as it requires a malicious or a compromised owner

**Description**

The `unstake` and `claim` methods in `FlorinStaking` have a `whenNotPaused` modifier and the same is true for the `redeem` and `_withdraw` methods in `LoanVault`. This opens up an attack vector, where the protocol owner can decide if the users are able to withdraw/claim any funds from it. There is also the possibility that an admin pauses the contracts and renounces ownership, which will leave the funds stuck in the contract forever.

**Recommendations**

Remove the `whenNotPaused` modifier from user exit/claim methods in the protocol or reconsider the `Pausable` integration in the protocol altogether.
