---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-2-3
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-L-4 Hard-coding Uniswap path assumptions
vuln_class: []
---

# TRST-L-4 Hard-coding Uniswap path assumptions

_Section severity (from Solodit section header): Low_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In NyPtvFantomWftmBooSpookyV2StrategyToUsdc.sol, estimateHarvest() is used to check if 
harvesting is profitable.
```solidity
      function estimateHarvest() external view override returns (uint256 profit, uint256 callFeeToUser) {
         uint256 pendingReward = 
         IMasterChef(SPOOKY_SWAP_FARM_V2).pendingBOO(POOL_ID, address(this));
            uint256 totalRewards = pendingReward + 
      IERC20Upgradeable(BOO).balanceOf(address(this));
      if (totalRewards != 0) {
         profit += 
      IUniswapV2Router02(SPOOKY_ROUTER).getAmountsOut(totalRewards, booToUsdcPath)[1];
      }
               profit += IERC20Upgradeable(USDC).balanceOf(address(this));
            uint256 usdcFee = (profit * totalFee) / PERCENT_DIVISOR;
         callFeeToUser = (usdcFee * callFee) / PERCENT_DIVISOR;
      profit -= usdcFee;
      }
```
Note that the code assumes `getAmountsOut()` will return USDC amount at index [1]. That is 
indeed the case right now, as **booToUsdcPath = [BOO, USDC];** However, it is an unnecessary 
coupling in code. `_swapFarmEmissionTokens()` handles the path correctly:

```solidity
            uint256[] memory amounts = 
         IUniswapV2Router02(SPOOKY_ROUTER).getAmountsOut(booBalance, booToUsdcPath);
      uint256 amountOutMin = (amounts[amounts.length - 1] * MAX_SLIPPAGE) / PERCENT_DIVISOR;
```

**Recommended mitigation**
Make the code more futureproof by refactoring `estimateHarvest()` to act similarly to 
`_swapFarmEmissionTokens()`.

**Team response**
Accepted, updated
