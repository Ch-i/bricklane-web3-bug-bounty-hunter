---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-03-06-radiant-capital-0-4
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2022-03-06T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md
tags:
- firm:zokyo
- report:2022-03-06-radiant-capital
title: Possible frontrun via flashloan attack.
vuln_class: []
---

# Possible frontrun via flashloan attack.

_Section severity (from Solodit section header): High_  
_Audit firm: Zokyo_  
_Source report: [2022-03-06-Radiant Capital.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-03-06-Radiant%20Capital.md)_

---

**Description**

Uniswap PoolHelper.sol: swap(), line 188. 
LiquidityZap.sol: addLiquidityWETHOnly(), line 113; addLiquidityETHOnly(), line 147. 
BalancerPoolHelper.sol: swap(), line 311. 
The contract does not check the actual amountOut' value during the tokens swap. Usually, the swap in protocols such as Uniswap or Balancer requires a parameter 'minimumLiquidity` and checks an actual output amount of token so that it will be not less than minimumLiquidity'. This parameter is essential in order to protect users from too high slippage and possible manipulations of the pool's reserves through frontrun. It is highly recommended to check the 'amountOut' and protect users from any possible pool manipulations. 

**Recommendation**: 

Pass 'minimumLiquidity as a function parameter and check that amountOut is greater or equal to 'minimum Liquidity`. 

**Post-audit**. 

The main function of LockZap.sol contains a slippage check. As for other contracts, it was verified by the Radiant team, that users shouldn't interact with LiquidityZap, BalancerPoolHelper, Uniswap PoolHelper directly.
