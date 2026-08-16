---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2023-06-09-narwhal-finance-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2023-06-09T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md
tags:
- firm:zokyo
- report:2023-06-09-narwhal-finance
title: Methods returning price in the wrong units
vuln_class: []
---

# Methods returning price in the wrong units

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2023-06-09-Narwhal Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2023-06-09-Narwhal%20Finance.md)_

---

**Severity**: High

**Status**: Resolved

**Description**

In TradingVaultV2.sol - Method getPricePerFullShare() starts by assuming 18 decimal places for price (i.e. at totalSupply() = 0) . Once totalSupply() takes non-zero value the method returns the decimals of USDT (i.e. which is 6 on arbitrum). That causes a severe mismatch that shall in turn affect the tokenomics.
Similarly in method deposit(), we have :
```solidity
if (totalSupply() == 0) {
    shares = _amount;
} else {
    shares = (_amount.mul(totalSupply())).div(currentBalanceUSDT);
}
```
_amount and currentBalanceUSDT refer to USDT quantities, hence they are 6 decimals. While totalSupply() refers to the NarwhalTradingVault which is 18 decimals. Therefore we end up having shares possessing 6 decimals at totalSupply() == 0 and 18 decimals otherwise.

**Recommendation** 

Adjust the units returned to be consistent in both cases (totalSupply() =0 or totalSupply() > 0).

**Fix**:  As  of commit 32d6f65  , Issue still not fixed despite attempts to address it. 

The current result we get from this part of the codebase: 
```solidity
if (totalSupply() == 0) {
    shares =  1e6  // _amount refers to USDC decimals
} else {
    shares =  1e18    // 1e6 * 1e18 / 1e6 = TradingVaultV2 decimals
} 
```
Here _amount  inside the if-branch needs to be scaled properly to match the units of TradingVaultV2. 

Where as  getPricePerFullShare()   we face this result:
 ```solidity
totalSupply() == 0 ? 1e6 : 1e6 * 1e6 /  1e18;  
```
As balance() refers to currentBalanceUSDT  which is 6 decimal places. Inconsistency across branches need to be addressed.
**Fix**:  Issue still not addressed as of commit 3998b5, the following is a response to partner’s point:  
 totalSupply simply in the order of 1e18 because the NarwhalTradingVault  as an ERC20 , is implementing the decimals() default ERC20 method inherited by NarwhalTradingVault  contract :
 ```solidity
   function decimals() public view virtual override returns (uint8) {
        return 18;
    }
```
Therefore, decimals of NarwhalTradingVault is 18 which is reflected in totalSupply .
Here's an example of how it's being dealt with from another project:


**Fix**: As of commit  0ee6199 

Issue mentioned in deposit(uint,address) function is fixed by introducing a factor to scale up the deposited amount to suit the shares being minted.


Regarding  getPricePerFullShare() function 


There’s an issue in:
totalSupply() == 0 ? 1e18 : balance().mul(1e18).div(totalSupply());
It is suggested to have either units of 1e18 in both cases or 1e6 in both cases.
What is shown now is that it is in units of 1e18 in case totalSupply()==0 .  And it is in units of 1e6 otherwise.


**Recommendation**: 


totalSupply() == 0 ? 10**USDT.decimals(): balance().mul(1e18).div(totalSupply());

**Fix**:  issue resolved in commit 6d90f9f
