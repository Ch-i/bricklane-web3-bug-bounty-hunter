---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-04-01-moleculevesting-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2023-04-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md
tags:
- firm:pashov-audit-group
- report:2023-04-01-moleculevesting
title: '[M-01] The `revoke` mechanics are not compatible with tokens that implement
  a block list feature'
vuln_class: []
---

# [M-01] The `revoke` mechanics are not compatible with tokens that implement a block list feature

_Section severity (from Solodit section header): Medium_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-04-01-MoleculeVesting.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-04-01-MoleculeVesting.md)_

---

**Impact:**
High, as important functionality in the protocol won't work

**Likelihood:**
Low, as a special type of ERC20 token has to be used as well as the attacker's address has to be in a block list

**Description**

Some tokens, for example `USDC` and `USDT` implement an admin controlled address block list. All transfers to a blocked address will revert. Since the `revoke` functionality forcefully transfers the claimable vested tokens to an address with a `vestingSchedule`, all calls to `revoke` will revert if such an address has claimable balance and is in the token's block list.

**Recommendations**

Use the [Pull over Push](https://fravoll.github.io/solidity-patterns/pull_over_push.html) pattern to send tokens out of the contract in a `revoke` scenario.
