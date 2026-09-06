---
affected_contracts: []
derives_from: []
id: solodit-trust-security-2023-01-19-lyra-finance-1-2
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-01-19T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md
tags:
- firm:trust-security
- report:2023-01-19-lyra-finance
title: TRST-M-3 base to quote swaps trust GMX-provided minPrice and maxPrice to be
  correct, which may be manipulated
vuln_class: []
---

# TRST-M-3 base to quote swaps trust GMX-provided minPrice and maxPrice to be correct, which may be manipulated

_Section severity (from Solodit section header): Medium_  
_Audit firm: Trust Security_  
_Source report: [2023-01-19-Lyra Finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Trust%20Security/2023-01-19-Lyra%20Finance.md)_

---

**Description:**
exchangeFromExactBase() in GMXAdapter converts an amount of base to quote. It 
implements slippage protection by using the GMX vault’s getMinPrice() and getMaxPrice() 
utilities. However, such protection is insufficient because GMX prices may be manipulated. 
Indeed, GMX supports “AMM pricing” mode where quotes are calculated from Uniswap 
reserves. A possible attack would be to drive up the base token (e.g. ETH) price, sell a large 
ETH amount to the GMXAdapter, and repay the flashloan used for manipulation. 
exchangeFromExactBase() is attacker-reachable from LiquidityPool’s exchangeBase().
```solidity
    uint tokenInPrice = _getMinPrice(address(baseAsset));
        uint tokenOutPrice = _getMaxPrice(address(quoteAsset));
    ...
    uint minOut = tokenInPrice
      .multiplyDecimal(marketPricingParams[_optionMarket].minReturnPercent)
        .multiplyDecimal(_amountBase)
          .divideDecimal(tokenOutPrice);
```

**Recommended Mitigation:**
Verify `getMinPrice()`, `getMinPrice()` outputs are close to Chainlink-provided prices as done in 
`getSpotPriceForMarket()`.

**Team Response:**
Fixed for `exchangeFromExactBase()` here, by using Chainlink price instead of **gmxMinPrice** of 
**baseAsset**. This way if the price is favorable for the LPs (given they rely on CL) it will not revert.
