---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[M-03] Owner has the power to zero-out user''s daily interest on rewards'
vuln_class: []
---

# [M-03] Owner has the power to zero-out user's daily interest on rewards

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as users can lose their right to claim accrued rewards

**Likelihood:**
Low, as it requires a malicious/compromised owner

**Description**

The `setDepositsActive` method resets `startTimestamp` and `lastGlobalUpdate`. The owner can front-run each `claimReward` transaction and by resetting the `startTimestamp` this will result in 0 `requiredRebases` in `calculateShareFromTime`, so the user will lose on his daily interest. On the other side, by resetting `lastGlobalUpdate` this will make `updateGlobalShares` never do a rebase, which will never inflate the `overallShare` which also shouldn't be possible.

**Recommendations**

Make the `setDepositsActive` method callable only once after contract deployment.
