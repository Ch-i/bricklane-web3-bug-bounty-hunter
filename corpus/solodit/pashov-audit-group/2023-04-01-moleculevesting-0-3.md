---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-moleculevesting-0-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-moleculevesting
title: '[M-04] Users won''t be able to claim vested tokens when contract is paused'
vuln_class: []
---

# [M-04] Users won't be able to claim vested tokens when contract is paused

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-MoleculeVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md)_

---

**Impact:**
High, as owner has the power to make it so that users can't claim any vested tokens

**Likelihood:**
Low, as it requires a malicious or a compromised owner

**Description**

The owner can currently execute the following attack:

1. Call `setPaused` with `paused == true`, so pause the contract
2. Now all user calls to `releaseAvailableTokensForHolder` will fail, since it has the `whenNotPaused` modifier
3. He can not unpause the contract forever or even renounce ownership

This is a common centralization problem which means the contract owner can "rug" users.

**Recommendations**

Remove the `whenNotPaused` modifier from `releaseAvailableTokensForHolder`, so users can claim vested tokens even if admin pauses the contract.
