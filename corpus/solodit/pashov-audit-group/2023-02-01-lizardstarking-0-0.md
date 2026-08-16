---
affected_contracts: []
derives_from: []
id: solodit-pashov-audit-group-2023-02-01-lizardstarking-0-0
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-02-01T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md
tags:
- firm:pashov-audit-group
- report:2023-02-01-lizardstarking
title: '[C-01] It''s impossible for a user to claim his rewards, as `claimReward`
  will never send out `USDC`'
vuln_class: []
---

# [C-01] It's impossible for a user to claim his rewards, as `claimReward` will never send out `USDC`

_Section severity (from Solodit section header): High_  
_Audit firm: Pashov Audit Group_  
_Source report: [2023-02-01-LizardStarking.md](https://github.com/solodit/solodit_content/blob/main/reports/Pashov%20Audit%20Group/2023-02-01-LizardStarking.md)_

---

**Impact:**
High, because users will never receive rewards from the contract

**Likelihood:**
High, because the code just uses the ERC20 API incorrectly

**Description**

The `claimReward` method should be used by a staker to receive `USDC` rewards for his locked NFTs. This won't ever work, as the transfer of the rewards is implemented with this code:

```solidity
USDc.transferFrom(msg.sender, address(this), claimableRewards);
```

This is wrong as it will transfer `USDC` from the staker to the staking contract instead of the other way around.

**Recommendations**

Change the code in the following way:

```diff
- USDc.transferFrom(msg.sender, address(this), claimableRewards);
+ USDc.transfer(msg.sender, claimableRewards);
```

Make sure to always use the ERC20 API correctly and also to have complete code coverage with unit tests of the codebase prior to having an audit.
