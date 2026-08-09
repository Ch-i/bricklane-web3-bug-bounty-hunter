---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-10-16-isle-finance-1-3
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-10-16T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md
tags:
- firm:zokyo
- report:2024-10-16-isle-finance
title: The redeem() function reverts on valid values of shares
vuln_class: []
---

# The redeem() function reverts on valid values of shares

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2024-10-16-Isle Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-10-16-Isle%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved

**Description**: 

In Pool.sol, the redeem() function does not allow any value of shares as a parameter to be passed other than a value equal to lockedShares. This is because, redeem() function calls processRedeem() from PoolConfigurator, which itself calls processExit() from WithdrawalManager. 
Line: 200 in Pool.sol
```solidity
 (redeemableShares_, assets_) = IPoolConfigurator(configurator).processRedeem(shares_, owner_, _msgSender());
```
Line: 228 in PoolConfigurator.sol
```solidity
(redeemableShares_, resultingAssets_) = _withdrawalManager().processExit(shares_, owner_);
```
Now in this processExit() function, there is an if statement on line:252 which uses strict equality (or inequality here) which results in a revert if requestedShares_ is not equal to the lockedShares. 
Line: 252 in WithdrawalManager.sol
```solidity
       if (requestedShares_ != lockedShares_) {   
           revert Errors.WithdrawalManager_InvalidShares(owner_, requestedShares_, lockedShares_);
       }
```
        But this strict inequality results in the pool.redeem(uint256 shares) to fail for any value of shares other than lockedShares_. 
        Ideally this is not expected as the function should work for any valid value of shares which can be set to any value as a parameter shares_ of the redeem() function.

**Recommendation**: 

It is advised to change the if statement to > instead of != on line: 252 of WithdrawalManager.sol's processExit() function. Also review the business logic and operational logic for the said changes.
