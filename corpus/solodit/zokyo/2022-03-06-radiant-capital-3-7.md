---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-3-7
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: 'Available borrows Ether is not calculated for an actual borrower. LockZap.sol:  _executeBorrow().'
vuln_class: []
---

# Available borrows Ether is not calculated for an actual borrower. LockZap.sol:  _executeBorrow().

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Function_execute Borrow() has a parameter '_onBehalf for which the availability of ETH to borrow is checked. However, the contract performs the actual borrow for msg.sender, which might mismatch with onBehalf parameter in case the function is called within zapWETH(). Because the user can pass an arbitrary '_onBehalf to zapWETH() function, removing this parameter and using msg.sender directly is recommended. The issue is marked as info, since LendingPool.sol still won't let borrow more than is available for msg.sender. 

**Recommendation**: 

Remove parameter_onBehalf and use msg.sender directly so that availability of Ether is checked for correct user. 

**Post-audit**: 

Availability is checked for '_onBehalf address. Since liquidity is staked for '_onBehalf, this might not be an issue that anyone can pass onBehalf and zap his funds (In case _onBehalf allowed LockZap to perform borrow on his behalf.)
