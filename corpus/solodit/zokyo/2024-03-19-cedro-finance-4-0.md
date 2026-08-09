---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-03-19-cedro-finance-4-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-03-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md
tags:
- firm:zokyo
- report:2024-03-19-cedro-finance
title: Import not being used
vuln_class: []
---

# Import not being used

_Section severity (from Solodit section header): Medium_  
_Audit firm: Zokyo_  
_Source report: [2024-03-19-Cedro Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-03-19-Cedro%20Finance.md)_

---

**Severity**: Informational

**Status**: Resolved


In Contract Pool.sol, OwnableUpgradeable is imported but not used.
In Contract LzRoute.sol (Branch), OwnableUpgradeable is imported but not used.

**Recommendation**: Remove unused imports.



### Incorrect comments / Typos / NatSpec comments issue

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract LzRoute.sol (Branch), the comment for the `_blockingLzReceive()` method is incorrect as the cross-chain message can be from the root chain only.

Across the protocol in `initialize ()` method, the comment for `roleManagerAddress` is incorrect as it is a contract, not an EOA.

In Contract Core.sol, the method `handleTransfer()` natspec 3rd param has a typo.

In Contract CEToken.sol, the method ) natspec 1st param has an incorrect comment as it core address, not the role manager address.

In Contract Branch.sol, the internal method `_pay(...)` missing natspec comment for few parameters.

In Contract LiquidationManager.sol, the method `liquidate(...)` has a typo 
```
) revert ClosingFactotExceeded(TAG);
```
 Should be
 ```
) revert ClosingFactorExceeded(TAG);
```

In Contract LiquidationManager.sol, the method liquidate(...) has a wrong comment 
// mint and burn CEToken and DebtToken then update supply
It should be
// burn and burn CEToken and DebtToken then update supply

**Recommendation**: Update the incorrect comments/typos/natspec comments


### Protocol uses a variety of roles

**Severity**: Informational

**Status**: Acknowledged

**Description**


Across the protocol, several roles are used to perform key operations, and assigning one such role to any unwanted address or any role account turning malicious can lead to unexpected results for the protocol.

**Recommendation**: 

It is advised to assign roles to as minimum accounts as possible. Make sure to revoke roles when not needed.



### Repay `params.tokenAmount` should be greater than `params.repayAmount`

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract Core.sol, the method `repay(...)` allows a user to deposit any extra amount more than the repay amount. However, the check is as follows:
```solidity
if (params.tokenAmount >= params.repayAmount) {
           ceAmount = params.tokenAmount.sub(params.repayAmount).mul(1e18).div(
               params.ceScaled
           );
 …. }
```
Here `params.tokens` should be more than `params.repayAmount` to check the `ceAmount`.

**Recommendation**: 

update the above condition as following
```solidity
if (params.tokenAmount > params.repayAmount) { … }
```







### ceTokens `_transfer()` does not check for dead chains

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract CeToken.sol, the internal method `_transfer(...)` does not check while transferring tokens if any chain is dead or not.

```solidity
for (uint256 i; i < chainIds.length; i++) {
           amountPerChain = balancePerChain[from][chainIds[i]]
               .mul(ceAmount)
               .div(ceTokenBalance);
           balancePerChain[from][chainIds[i]] -= amountPerChain;            balancePerChain[to][chainIds[i]] += amountPerChain;
           transferCeAmount += amountPerChain; // for handling precision
           if (balancePerChain[from][chainIds[i]] == 0)
               _removeChain(from, chainIds[i]);
           _addChain(to, chainIds[i]);
       }
```
Here a user can transfer another user tokens from dead chains affecting the withdrawable capacity of the later.

Also, it is not checked if `amountPerChain >= balancePerChain[from][]chainIds[i]` before the following operation;
```
balancePerChain[from][chainIds[i]] -= amountPerChain; 
```
This can lead to an underflow panic error with transaction reverting without any reason.

**Recommendation**: 

It is advised to add a check if there is enough `balancePerChain` for the user before deducting the `amountPerChain` as done in `burn(...)` and `liquidate(...)` amount. 


### External call to unknown contract

**Severity**: Informational

**Status**: Acknowledged

**Description**

Contract `CEToken` and `DebtToken` make external calls to `rewardController` address in the `handleReward()` internal method. Since the inner workings of this contract are unknown, it is risky and can lead to unexpected results.

**Recommendation**: 

It is advised to make external calls to trusted contracts only.



### Missing `nonreentract` modifier

**Severity**: Informational

**Status**: Resolved

**Description**

In Contract Branch.sol, the method `transferTokens()` allows to transfer ETH to the recipient address which can result in a callback. 
```solidity
if (token == address(0)) {
           (bool sent, ) = payable(receipient).call{value: localAmount}("");
           if (!sent) revert NativeTransferFailed(TAG);
       } else {
           IERC20Upgradeable(token).safeTransfer(receipient, localAmount);
       }
```

**Recommendation**: 

It is advised to add `nonreentrant` modifier to the `transferTokens()` method.


### Method `loop()` is inherently risky for users

**Severity**: Informational

**Status**: Acknowledged

**Description**

In Contract Pool.sol, the method `loop(..)` can be used to leverage collaterals to borrow and deposit the same assets in loops to earn fees/rewards.

This is risky because during the process market fluctuations can lead to the liquidation of the collateral deposited along with no borrowed assets. So in this situation, a user is left with no collateral and no borrowed assets.

**Recommendation**: 

It is recommended to acknowledge and advise accordingly to the users.

### Oracle prices fetched from DEXs can be manipulated 

**Severity**: Informational

**Status**: Resolved

**Description**

When fetching a price from an Oracle, it is advisable to minimize the reliance on prices obtained from Decentralised Exchanges (DEXs), as these prices are susceptible to manipulation. Currently, the contract allows fetching prices from both DEXs and Chainlink oracles. The potential vulnerability lies in the fact that DEX prices can be manipulated, which may lead to incorrect price data being used 

**Recommendations**:

Implement Price Deviation Check: Introduce a mechanism to compare prices obtained from DEXs with those from Chainlink. If the deviation exceeds a predetermined threshold (e.g., 5%), further verification or corrective measures should be initiated. This approach aims to ensure that the prices used by the Oracle are within a reasonable range of the more stable and less manipulable Chainlink prices.
Time-Interval Checks for Price Updates: Setting a longer time interval (e.g., 600 seconds) between price updates can deter manipulation by increasing the cost and effort required to influence prices consistently over time.
Note# We will use chainlink as primary oracle source and dex will be only used as fallback option when the chainlink malfunctions. So the dex comparison with chain link will not make sense in our oracle contract.

### Usage of Unchecked in TickMath and FullMath

**Severity**: Informational

**Status**: Acknowledged

It can be seen that unchecked block has been used in calculations of FullMath and TickMath. It is not recommended to use unchecked math as it can lead to wrapping, overflowing and underflowing risks. 

**Recommendation**: 

It is recommended to stick to using the checked math only.

**Comments**: 

The client said that they had used it in order to lower gas fees.

### Layerzero best practices not followed 

**Severity**: Informational

**Status**: Acknowledged 


This is missing check for payload size in LzApp.sol. As a result, it can lead to a large payload size being executed or undesired payload size being executed leading to unintended issues.

Additionally, `ILayerZeroUserApplicationConfig()` has been imported but it has not been used or inherited in the LzApp.sol contract. It is advised to inherit it and implement it according to the best practices of Layerzero. It is advised to implement ILayerZeroUserApplicationConfig interface in the LzApp, including the `forceResumeReceive()` function which, in the worst case can allow the owner/multisig to unblock the queue of messages if something unexpected happens.

Also there is missing `setMinDstGasa()` function  in the LzApp.
The function call on the destination chain requires a specific amount of gas or, otherwise, it will revert with out-of-gas exception.

It is the User Application’s responsibility to make sure that there are correct limits set that will instruct relayers to specify the correct amount of gas at the source chain to prevent users from inputting too low the value for gas.

Especially, when the application supports multiple message types it is recommended to specify the minimum amount of gas for each of them. The minimum amounts of gas can be set using the setMinDstGas function in LzApp contract.

Additionally, you can use custom adapter parameters (_adapterParams) to specify the gas limits for each call. When specifying the gas, one must not forget about fees that cover that. You can get the fees using estimateFees function from the endpoint contract. 

Refer these for more info- https://layerzero.gitbook.io/docs/layerzero-tooling/best-practice and https://composable-security.com/blog/secure-integration-with-layer-zero/ 

**Recommendation**: It is advised to follow best practices for Layerzero as mentioned above.

### Double assignment in LzRouteV2

**Severity**: Informational

**Status**: Resolved

**Description**

In LzRouteV2 of the Branch folder, the variable executorGas has been initialized twice in the constructor. First on line 45 and then on line: 49. 

**Recommendation**: 

It is advised to initialize the variable only once.

### Missing events for critical functions

**Severity**: Informational

**Status**: Acknowledged

**Description**

Missing events for critical functions such as `setRoleManager()` function in Branch.sol and `setRoleManager()` function of Pool.sol. 

**Recommendation**: 

It is advised to emit events for critical state changes, as emitting events would be a best practice for offchain monitoring.

**Comments**: 

The client said that the required events utilized by backend are added.
