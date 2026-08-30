---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-florence-finance-2-4
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-florence-finance
title: '[M-05] The protocol uses `_msgSender()` extensively, but not everywhere'
vuln_class: []
---

# [M-05] The protocol uses `_msgSender()` extensively, but not everywhere

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-Florence Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-Florence%20Finance.md)_

---

**Impact:**
Low, because protocol will still function normally, but an expectedly desired types of transactions won't work

**Likelihood:**
High, because it is certain that he issue will occur as code is

**Description**

The code is using OpenZeppelin's `Context` contract which is intended to allow meta-transactions. It works by using doing a call to `_msgSender()` instead of querying `msg.sender` directly, because the method allows those special transactions. The problem is that the `onlyDelegate` and `onlyFundApprover` modifiers in `LoanVault` use `msg.sender` directly instead of `_msgSender()`, which breaks this intent and will not allow meta-transactions at all in the methods that have those modifiers, which are one of the important ones in the `LoanVault` contract.

**Recommendations**

Change the code in the `onlyDelegate` and `onlyFundApprover` modifiers to use `_msgSender()` instead of `msg.sender`.
