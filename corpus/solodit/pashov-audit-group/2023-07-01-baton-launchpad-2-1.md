---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-07-01T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md
tags:
- firm:pashov-audit-group
- report:2023-07-01-baton-launchpad
title: '[L-02] The `refund` mechanism can be used by accounts with allowances'
vuln_class: []
---

# [L-02] The `refund` mechanism can be used by accounts with allowances

_Section severity (from Solodit section header): Low_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

The `refund` method calls `_burn` which would allow burning a token if you have allowances for it. While this is a highly unlikely scenario to occur as it also requires the `msg.sender` to have `totalMinted` and `availableRefund` values in the `_accounts` mapping, it is still a logical error. Allow only the owner of the `tokenIds` to execute a `refund` on them.
