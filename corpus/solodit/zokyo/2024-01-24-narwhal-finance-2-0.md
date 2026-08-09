---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2024-01-24-narwhal-finance-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-01-24T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2024-01-24-narwhal-finance
title: Possibility of inflation of `totalAssets` through direct donation
vuln_class: []
---

# Possibility of inflation of `totalAssets` through direct donation

_Section severity (from Solodit section header): Low_  
_Audit firm: Zokyo_  
_Source report: [2024-01-24-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2024-01-24-Narwhal%20Finance.md)_

---

**Severity**: Low

**Status**: Acknowledged 

**Description**

The deposit function from the Vault contract allows users to deposit a specified amount of assets into the vault. Upon a successful deposit, the user's asset amount is updated, and shares are minted based on the current total value of the vault. Users can withdraw their assets from the vault through the withdraw function. It calculates the amount of assets corresponding to the user’s shares and then performs the withdrawal, reducing the user’s share count. 
The `convertToShares` and `convertToAssets` functions allow the conversion between assets and shares based on the total value of the vault and the total supply of shares. This calculation is based on the value returned by the totalAssets function, which returns the current balance of assets held by the contract.

The vulnerability arises from the ability to inflate the totalAssets value through direct donations to the contract's address, bypassing the deposit function. An attacker can transfer assets directly to the contract, thereby increasing the balance of assets without the corresponding minting of shares. This inflation impacts the calculation of share value for subsequent legitimate deposits, leading to these users receiving fewer or even zero shares. The attacker can then withdraw their assets immediately after a user's legitimate transaction, obtaining the inflated value of the assets.

**Recommendation**: 

Implement a mechanism to track assets separately from the contract's direct balance.
Ensure that a user receives more than 0 shares for their deposit.


**Client Comment** : Our vault contract operates in two phases. In the "mint" phase, when a user deposits USDT, we mint Vault tokens at a 1:1 ratio and allocate them to the user. There is a minimum minting amount for each user, and they must reach a certain threshold to progress to the next stage, the "deposit" phase. During this phase, the Vault contract's USDT balance is calculated, and Vault tokens are minted for the user based on their deposit proportion. Similarly, there is a minimum deposit requirement. Therefore, transferring USDT to the Vault contract during the "mint" phase results in losses without any gains. In the "deposit" phase, although it may affect the proportion, this is considered normal logic. Attackers would incur greater losses with minimal gains. Additionally, our withdrawal logic allows withdrawals only at a designated time, not at any time. There are also limits on the deposit amounts for each user and an overall limit on the vault's total deposits. Considering the scenarios mentioned in the report, it seems unlikely to occur.
