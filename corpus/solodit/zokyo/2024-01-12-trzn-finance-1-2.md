---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-12-trzn-finance-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-01-12T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md
tags:
- firm:zokyo
- report:2024-01-12-trzn-finance
title: Centralization risk
vuln_class: []
---

# Centralization risk

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-01-12-TRZN Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-12-TRZN%20Finance.md)_

---

**Severity**: Medium

**Status**: Acknowledged

**Description**

In Contract VaultETH_V2, there are several methods using the modifier `onlyRole(DEFAULT_ADMIN_ROLE)` which can be used to configure important parameters for the protocol such as oracles, WETH, etc. But in the constructor, DEFAULT_ADMIN_ROLE is being set to msg.sender which is an EOA.

There is also an emergencyWithdraw method which allows DEFAULT_ADMIN_ROLE to withdraw all the deposited ETH in the vault.

This risks the whole protocol being centralized and controlled by a single EOA.

**Recommendation** 

It is advised to decentralize the usage of these functions by using a multisig wallet with at least 2/3 or a 3/5 configuration of trusted users. Alternatively, a secure governance mechanism can be utilized for the same. 

**Client comment**: We originally planned to deploy multi-sig and update it in the future by replacing the admin address with multi-sig. If you would recommend ways to improve contract code stability, we would appreciate it so we may consider how to improve.
