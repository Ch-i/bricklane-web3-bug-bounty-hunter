---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-2-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Vesting schedule can be overwritten and parameters are not validated.
vuln_class: []
---

# Vesting schedule can be overwritten and parameters are not validated.

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

TokenVesting.sol: addVest(). 
The owner is able to overwrite vesting, which is already ongoing. Any tokens from the previous vesting that weren't already claimed will get stuck on the contract. Though only the owner can call this function, already existing vestings can still be overwritten, leading to the loss of funds. Also, to prevent invalid vesting creation, it is recommended to validate parameters_amount' and '_duration against zero values, as in case '_duration' is zero, RDNT tokens still will be transferred. However, the claimer couldn't claim them due to validation in function claim(), line 53. 

**Recommendation**: 

Do not allow to overwrite vesting schedules which are already in progress and validate parameters_amount' and '_duration' not to be zero values. 

**Post-audit**: 

Parameters are validated and active vesting can't be overwritten.
