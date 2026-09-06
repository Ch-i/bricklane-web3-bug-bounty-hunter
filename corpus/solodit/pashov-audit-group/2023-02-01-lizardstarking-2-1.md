---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-2-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[M-02] Missing constraint on the setter method of a percentage value'
vuln_class: []
---

# [M-02] Missing constraint on the setter method of a percentage value

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, as it will result in wrong reward calculations

**Likelihood:**
Low, as it requires a malicious/compromised owner or a big error on his side

**Description**

The `setResetShareValue` lacks a check that the `_newShareResetValue` argument is not more than 100%. Since it is expected that the value will be in percentages, setting a value that is bigger than 100 will mess with the important calculations in the contract, one of which is the rewards to claim calculation. This can make users receive a smaller reward than what they have earned since a bigger `resetShareValue` equals smaller rewards for users.

**Recommendations**

Add a check in `setResetShareValue` that the `_newShareResetValue` argument is not more than 100%.
