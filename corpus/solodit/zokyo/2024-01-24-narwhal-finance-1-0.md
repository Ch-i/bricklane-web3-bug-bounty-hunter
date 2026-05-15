---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Division by Zero in `_getNextClaimableAmount` Function
vuln_class: []
---

# Division by Zero in `_getNextClaimableAmount` Function

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**:

The `VestingSchedule` contract, particularly in its `_getNextClaimableAmount` function, is vulnerable to a division by zero error. This issue occurs when `groupVestingDuration[addressGroup[_account]]` is zero, a scenario that might not be uncommon, especially if vesting durations for certain groups are not set correctly or are inadvertently set to zero. The division by zero can lead to a panic error, causing contract execution to fail and potentially locking funds.
**Scenario:**
An account is added to the vesting schedule with a specific group.
The group's vesting duration is either not set or mistakenly set to zero.
The account tries to claim vested tokens.
The contract attempts to calculate the claimable amount using groupVestingDuration[addressGroup[_account]] which is zero, leading to a division by zero error.
This scenario can occur during regular operation, particularly in cases where new vesting groups are added without proper validation of input parameters.

**Recommendation:**

Implement the following changes to mitigate this vulnerability:
Input Validation: Ensure that groupVestingDuration is never set to zero in the addGroupCliff function. Add checks to prevent setting a zero vesting duration.
Safe Division: In _getNextClaimableAmount, before performing the division, check if groupVestingDuration[addressGroup[_account]] is zero. If it is, handle this case by either returning zero or reverting with a clear error message.
