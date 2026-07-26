---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-6
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Lack of input validation in function
vuln_class: []
---

# Lack of input validation in function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In VestingSchedule.sol
Method addGroupCliff: _cliff is not validated to be non-zero value, having _cliff = 0 implies that it is not set to a value to begin with as shown in require(groupCliff[_group] == 0, ... ); which implies that it should be set only once for that given _group.
In that sense groupVestingDuration can be changeable for one given _group which leads to miscalculations as it gets involved in claimable amounts.
As for TradingVaultV2.sol - State _rewardsDuration is uint256, there is a chance a wrong large value is entered mistakenly. The consequences can lead to  DoS on setRewardsDuration() which in turn hinders the chance of handling the mistake by resetting the variable. That is because periodFinish would take a large value affected by the new value of _rewardsDuration.

**Recommendation** 

Add require statement to verify inputs are non-zero value.

Since _rewardsDuration is in order of years, it is recommended to have a maximum value around that value range. Then add a require statement to ensure that the _rewardsDuration is less than that maximum value.

**Fix**: As of  commit a72e06b , It is stated that _cliff can be zero for investors. The issue though is that it being stated in the revert message that groupCliff can not be changed if already set. But in this case groupCliff can be resettable if set to zero over and over which makes it severe because the vestingDuration can be altered in this scenario more than once. In order to counter that a new variable need to be introduced that shows if the groupCliff has been set already or not. 

The second part of the issue regarding TradingVaultV2.setRewardsDuration() is resolved by dev team.
**Fix**: As  of commit 32d6f65 , There is no change to address the issue in addGroupCliff().
**Fix**:  Fixed in 3998b5b,  by adding groupCliffSet to act as the check of whether the mapping groupCliff has been set for given _group or not.
