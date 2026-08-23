---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Lack of Validation in `addGroupCliff` Function
vuln_class: []
---

# Lack of Validation in `addGroupCliff` Function

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status** : Acknowledged 

**Description**:

The `addGroupCliff` function in the `VestingSchedule` smart contract is intended to set the cliff and vesting duration for different groups. However, it lacks comprehensive validation for the input parameters `_cliff` and `_vestingDuration`. Specifically, the function does not enforce reasonable ranges for these parameters nor does it ensure that the total vesting duration is equal to or greater than the cliff duration. This oversight allows for the setting of impractical or illogical values, potentially leading to functional issues within the contract.
**Scenario**:
The contract accepts a vesting duration that is shorter than the cliff duration, which contradicts standard vesting logic. For instance, a cliff of 1 hour and a vesting duration of 30 minutes is accepted without error.
Extremely large values for either parameter could be set, leading to impractical or unmanageable vesting schedules.

**Recommendations**:

Input Validation: Implement checks to ensure that _cliff and _vestingDuration are within practical ranges. This could include upper limits to prevent excessively long vesting periods.
Cliff and Vesting Duration Relationship: Add a validation rule to ensure that _vestingDuration is always equal to or greater than _cliff. This aligns with standard vesting practices and avoids logical inconsistencies.
