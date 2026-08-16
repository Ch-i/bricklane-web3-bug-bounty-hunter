---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-2-16
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Setting rewardsDuration to 0 can cause unexpected behavior
vuln_class: []
---

# Setting rewardsDuration to 0 can cause unexpected behavior

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Resolved


**Description**: 

The rewardsDuration variable in the NarwhalTradingVault & NarwhalPool contract determines the duration of the rewards period, which is used to calculate the reward rate and distribute rewards to users. However, if the owner sets rewardsDuration to 0, the calculation of periodFinish in the notifyRewardAmount function will result in the same value as block.timestamp, causing the rewards period to end immediately after starting. This can result in confusion and unexpected behavior, and may lead to a loss of funds if users are not aware of the issue and continue to stake their tokens.

**Impact**: 

A malicious actor could potentially exploit this vulnerability by setting rewardsDuration to 0 and then depositing a large amount of tokens to earn rewards for a short period of time. This could drain the reward pool and result in a loss of funds for users.

**Recommendation**: 

To mitigate this vulnerability, a check should be added to the setRewardsDuration function to ensure that rewardsDuration is not set to 0. Alternatively, the notifyRewardAmount function could be updated to set periodFinish to a minimum value if rewardsDuration is set to 0, to ensure that the rewards period is at least one block long. Additionally, users should be informed of the potential issue and advised to avoid staking their tokens if rewardsDuration is set to 0.

**Fixed**: Issue fixed in commit a72e06b by adding the range the issue is fixed
