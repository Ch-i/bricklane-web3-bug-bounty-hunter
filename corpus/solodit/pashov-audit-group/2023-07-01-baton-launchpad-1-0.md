---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-07-01-baton-launchpad-1-0
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
title: '[M-01] It''s not possible to execute a rewards migration of a `BatonFarm`'
vuln_class: []
---

# [M-01] It's not possible to execute a rewards migration of a `BatonFarm`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-07-01-Baton Launchpad.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-07-01-Baton%20Launchpad.md)_

---

**Severity**

**Impact:**
High, as it can lead to stuck rewards

**Likelihood:**
Low, as it is not likely that a migration is needed

**Description**

The `BatonFarm` contract which is an external dependency of the `Nft` contract (a `BatonFarm` is deployed in `seedYieldFarm`) has a migration mechanism to move the unearned rewards to a new contract. This functionality is currently blocked, because it depends on a call from the `BatonFarm` owner (the `Nft` contract in this case) to the `initiateMigration` method of `BatonFarm`. Since such a call is not possible as there is no code for it, migrations are currently impossible in the system. This means that if there are rewards left in a `BatonFarm` contract deployed by some `Nft` contract, they will be stuck there forever.

**Recommendations**

Add a way for the `Nft` admin to execute an `initiateMigration` call.
