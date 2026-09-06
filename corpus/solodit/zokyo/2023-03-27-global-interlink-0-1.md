---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-03-27-global-interlink-0-1
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-03-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md
tags:
- firm:zokyo
- report:2023-03-27-global-interlink
title: Whitelisted table balance and contract balance can be different resulting in
  locked funds for users
vuln_class: []
---

# Whitelisted table balance and contract balance can be different resulting in locked funds for users

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-03-27-Global Interlink.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-03-27-Global%20Interlink.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

At this moment, the whitelisted address are added through the add_to_whitelist method and the funds of the pool are added through the deposit functionality, however these 2 steps pattern can become problematic for the contract integrity and the vested users, as the contract admin can add in the whitelist table tokens amount that do not reflect the true token balances in the contract, and users could be stuck with uncorrelated/hypothetical funds because there would be nothing for them to release from vesting.

**Recommendation**: 

Implement a check to never being able to add more hypothetical total funds in the table then the ones in contract balance or every time admin add a new user to the whitelist also transfer the necessary vested funds for that user directly in the same function logic.
