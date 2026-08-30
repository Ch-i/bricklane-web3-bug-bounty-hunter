---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-0-6
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
title: Users Might Miss The Withdrawal Window While The Protocol Is Paused
vuln_class: []
---

# Users Might Miss The Withdrawal Window While The Protocol Is Paused

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity** - Low


**Status** - Acknowledged

**Description**: 

User withdrawals only happen in respective windows , which is current window +2  , but the user might miss the withdrawal window while the protocol was paused . The pausing mechanism does not extend the window time frame therefore if a user had his withdrawal window between x and y and the protocol was paused within this time frame , he would miss his window and now he has to remove some of his tokens when the protocol resumes in order to push his window to a new current window where he can withdraw.

Also, a loan might get subject to a default while the protocol was paused . In the paused state the user won’t be able to repay the loan and as soon as the system gets unpaused the loan is subject to a default and gets defaulted.

**Recommendation**:

Account for the paused timeframe within the withdrawal window or the users should be acknowledged of such behavior in advance.

**Client comment**: If for some reason the protocol must be temporarily paused, for example, if the pool admin is undergoing legal procedures to recover defaulted funds, we will inform users in advance that the protocol will be temporarily paused.
