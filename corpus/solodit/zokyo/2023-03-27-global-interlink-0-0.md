---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-0-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: Tx sender can steal the released tokens of any whitelisted user
vuln_class: []
---

# Tx sender can steal the released tokens of any whitelisted user

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: Critical

**Status**: Resolved

**Description**

In contract token_vesting.move, function `release` is having the role of releasing the vested funds, first the function is checking that the parameter ‘receiver’ is a whitelisted address and after that is proceeding to calculate the amount that will be vested, adjust the storage and transfer the tokens, however there is one problem, the user that is checked for being whitelisted and is having his amount calculated is the ‘receiver’ variable, but the account that will actually receive the tokens is the function caller, there is where the problem is at L#225, the tokens in the end are not transferred to the receiver address but to the account that have called the function, which can be the receiver or not 

**Recommendation**: 

Implement proper sanity check by making sure the tx sender have the same address with the receiver or do not pass the receiver variable through the function parameters and just assign it the address of the caller
