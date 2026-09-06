---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-15
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Inconsistent Calculation of Rewards Period
vuln_class: []
---

# Inconsistent Calculation of Rewards Period

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved

**Description**

setRewardsDuration and notifyRewardAmount functions in the NarwhalTradingVault & NarwhalPool contract. The problem is that the notifyRewardAmount function calculates the periodFinish variable and sets it based on the rewards duration, which can be modified by the setRewardsDuration function. This means that if the notifyRewardAmount function is called before the setRewardsDuration function, the calculated periodFinish value will not reflect the new rewards duration.
This can lead to an inconsistency in the rewards distribution and may result in an incorrect calculation of rewards earned by users. 

**Impact**:

Gov could potentially exploit this vulnerability by calling the notifyRewardAmount function with a large reward amount and then calling the setRewardsDuration function with a small duration. This would result in a higher reward rate than intended and could potentially drain the reward pool.

**Recommendation** 

 notifyRewardAmount function should not calculate the periodFinish variable and instead rely on the duration of the reward set by the setRewardsDuration function. Alternatively, the setRewardsDuration function could be updated to also update the periodFinish variable to reflect the duration of the new reward.
**Another fix **: 

if rewardsDuration is set to zero. In that case, the calculation of periodFinish will result in the same value as block.timestamp, which means that the rewards period will end immediately after starting. This could potentially cause confusion or unexpected behavior.
To avoid this issue, it would be better to add a check for rewardsDuration and throw an error or revert the transaction if it is set to zero. For example:

**Fixed**: Issue fixed in commit a72e06b by adding the range the issue is fixed 

The function has a requirement that the input _rewardsDuration must be within the range of 183 days to 730 days. If the value is outside of this range, the transaction will revert and the change will not be made.
