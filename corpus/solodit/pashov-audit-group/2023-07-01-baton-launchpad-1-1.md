---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-07-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md
tags:
- firm:pashov-audit-group
- report:2023-07-01-baton-launchpad
title: '[M-02] Possible front-running griefing attack on NFT creations'
vuln_class: []
---

# [M-02] Possible front-running griefing attack on NFT creations

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

**Severity**

**Impact:**
Medium, as it results in a temporary DoS for users of the protocol

**Likelihood:**
Medium, as it is easy to execute but attacker doesn't have much incentive to do it

**Description**

The `create` method in `BatonLaunchpad` calls the `cloneDeterministically` method from `LibClone` that uses the `create2` opcode. The `create` method also has a `salt` parameter that is passed to the `cloneDeterministically` call. A malicious actor can front-run every call to `create` and use the same `salt` argument. This will result in reverts of all user transactions, as there is already a contract at the address that `create2` tries to deploy to.

**Recommendations**

Adding `msg.sender` to the `salt` argument passed to `cloneDeterministically` will resolve this issue.
