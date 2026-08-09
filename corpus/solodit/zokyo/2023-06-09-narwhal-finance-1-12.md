---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-1-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Contract have been updated to be upgradeable lacks proper method to disable
  implementation contracts’ initialize(...) method
vuln_class: []
---

# Contract have been updated to be upgradeable lacks proper method to disable implementation contracts’ initialize(...) method

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: Medium

**Status**: Resolved

**Description**

In the latest commit a72e06b, several contracts have been made upgradeable using OpenZeppelin Upgradeable library.
Following are the contracts which are made upgradeable:
NarhwalRefferals
NarwhalTrading
NarwhalTradingCallbacks
TradingStorage
As it is recommended in OpenZeppelin’s documentation to not leave implementation contract uninitialised as attacker can take advantage of the same and that may affect the proxy contract. 
Because of the same reason, all of the above mentioned contracts use `disableInitializer()` method to disable the initialize() method. 
This approach does not resolve the issue completely and still put the risk of attacker taking control over the implementation contract. Let us look what happens when contracts are deployed.
When the proxy and implementation contract is deployed, initialization will be done in the context of proxy contract but not implementation contract.
Implementation contract will have  `storageT` as address(0) as it is not initialized.
Deployer can call `disableInitializers()` only if `gov` is set but it will revert as `storageT` is not set only.
Deployer will need to make a call to implementation contract’s `initialize(...)` method which can be front-run by Attacker to take control over the implementation contract.
Even if deployer is able to call the initialize(...) method, it will disable the initialize() method after the call. Deployer will not need to call `disableInitializers()` anymore to do so.
This is the exact reason why OpenZeppelin suggests to use the following:
```solidity
/// @custom:oz-upgrades-unsafe-allow constructor
constructor() {
_disableInitializers();
}
```
Using this approach will disable the initializers for the implementation contracts directly without any other transaction. The above approach is suggested as well to avoid being dependent on a transaction to disable the initializer or being front-run by attackers.
**Fixed**: Issue fixed in commit 3998b5b
