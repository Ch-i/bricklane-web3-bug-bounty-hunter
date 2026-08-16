---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-M-2 Attacker can force partial withdrawals to fail
vuln_class: []
---

# TRST-M-2 Attacker can force partial withdrawals to fail

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In Ninja vaults, users call `withdraw()` to take back their deposited tokens. There is 
bookkeeping on remaining amount:

```solidity
      uint256 userAmount = balanceOf(msg.sender);
         // - Underlying (Frontend ONLY)
            if (userAmount == 0) {
            user.amount = 0;
         } else {
         user.amount -= r;
      }
```
If the withdraw is partial (some tokens are left), user.amount is decremented by r.

```solidity
      uint256 r = (balance() * _shares) / totalSupply();
```
Above, r is calculated as the relative share of the user's _shares of the total balance kept in 
the vault.

We can see that user.amount is incremented in deposit().

```solidity
      function deposit(uint256 _amount) public nonReentrant {
      …
            user.amount += _amount;
      …
         }
```
The issue is that the calculated r can be more than _amount , causing an overflow in 
`withdraw()` and freezing the withdrawal. All attacker needs to do is send a tiny amount of 
underlying token directly to the contract, to make the shares go out of sync.

**Recommended Mitigation:**
Redesign **user** structure, taking into account that balance of underlying can be externally 
manipulated

**Team Response:**
Accepted after further investigation. we agreed to remove the double accounting 
(user.amount) and to dynamically calculate the value from the users share balance * price 
per share. We added the public view function getUserUnderlyingBalance to assist (which 
also allows dynamic underlying decimals).
