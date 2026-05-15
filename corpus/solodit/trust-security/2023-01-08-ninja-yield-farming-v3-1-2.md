---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-08-ninja-yield-farming-v3-1-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-01-08T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md
tags:
- firm:trust-security
- report:2023-01-08-ninja-yield-farming-v3
title: TRST-M-3 Rewards may be stuck due to unchangeable slippage parameter
vuln_class: []
---

# TRST-M-3 Rewards may be stuck due to unchangeable slippage parameter

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-08-Ninja Yield Farming v3.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-08-Ninja%20Yield%20Farming%20v3.md)_

---

**Description:**
In NyPtvFantomWftmBooSpookyV2StrategyToUsdc.sol, MAX_SLIPPAGE is used to limit 
slippage in trades of BOO tokens to USDC, for yield:
```solidity
      function _swapFarmEmissionTokens() internal { IERC20Upgradeable boo = IERC20Upgradeable(BOO);
            uint256 booBalance = boo.balanceOf(address(this));
      if (booToUsdcPath.length < 2 || booBalance == 0) {
         return;
      }
         boo.safeIncreaseAllowance(SPOOKY_ROUTER, booBalance);
             uint256[] memory amounts = 
      IUniswapV2Router02(SPOOKY_ROUTER).getAmountsOut(booBalance, booToUsdcPath);
          uint256 amountOutMin = (amounts[amounts.length - 1] * MAX_SLIPPAGE) / PERCENT_DIVISOR;
            IUniswapV2Router02(SPOOKY_ROUTER).swapExactTokensForTokensSupportingFeeOnTransferTokens( booBalance, amountOutMin, booToUsdcPath, address(this), block.timestamp );
                }
```
If slippage is not satisfied the entire transaction reverts. Since **MAX_SLIPPAGE** is constant, it 
is possible that harvesting of the strategy will be stuck, due to operations leading to too high 
of a slippage. For example, strategy might accumulate a large amount of BOO, or `harvest()` 
can be sandwich-attacked.

**Recommended Mitigation:**
Allow admin to set slippage after some timelock period.

**Team Response:**
Accepted. We converted MAX_SLIPPAGE to maxSlippage, a uint256 that the ADMIN Multisig 
role can update. We decided against a timelock, as we may need to change it once, unlock 
an individual harvest issue and put it back before the next harvest.
