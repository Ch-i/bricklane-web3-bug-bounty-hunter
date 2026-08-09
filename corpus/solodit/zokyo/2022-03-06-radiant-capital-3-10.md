---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-10
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Unnecessary validation checks and operations in Token Vesting.
vuln_class: []
---

# Unnecessary validation checks and operations in Token Vesting.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

TokenVesting.sol: initialize(), claim(). 
In TokenVesting.sol (line 29), the validation for msg.sender not being zero address is making no sense as zero address cant call any external methods. 
In TokenVesting.sol (line 66), the statement if(v.duration == 0) will never become true as zero duration could be set because of validation "duration>0" in the method for adding vesting. 

**Recommendation**: 

Remove useless validation and if-statement. 

**Post-audit**: 
Contract was removed.
