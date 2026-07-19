---
affected_contracts: []
derives_from: []
id: solodit-zachobront-2023-11-01-splits-oracle-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-11-01T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md
tags:
- firm:zachobront
- report:2023-11-01-splits-oracle
title: '[M-02] Tokens with extreme price differences along the path could round price
  to zero'
vuln_class: []
---

# [M-02] Tokens with extreme price differences along the path could round price to zero

_Section severity (from Solodit section header): Medium_  
_Audit firm: ZachObront_  
_Source report: [2023-11-01-splits-oracle.md](https://github.com/solodit/solodit_content/blob/main/reports/ZachObront/2023-11-01-splits-oracle.md)_

---

In the unlikely event that the price ratio between two tokens is more than `1e18:1`, the oracle will round the price down zero.

While the largest price ratio I can currently find is `BTC/SHIB` (which can be calculated using [SHIB/ETH](https://etherscan.io/address/0x8dD1CD88F43aF196ae478e91b9F5E4Ac69A97C61#readContract) and [ETH/BTC](https://etherscan.io/address/0xdeb288F737066589598e9214E782fa5A8eD689e8#readContract) to be approximately `1e11:1`), that puts us close enough to the range that this is something we should be prepared for.

Based on the use for this oracle with swappers, a `0` price would allow the bot executing the swap to steal all of a user's tokens for free.

Note that this `0` price could occur as an intermediate step along a longer path, and the `0` value would carry through to the final price, leading to the theft of tokens with closer values as well.

**Recommendation**

While rounding is inevitable with such a large price discrepancy and 18 decimals of precision, it is worth including an explicit check that `price != 0` to ensure that tokens cannot be stolen.

```diff
function _getQuoteAmount(QuoteParams calldata quoteParams_) internal view returns (uint256) {
    ...
    if (pd.inverted) price = WAD.divWadDown(price);
+   if (price == 0) revert ZeroPrice();
    return _convertPriceToQuoteAmount(price, quoteParams_);
}
```

**Review**

[Fixed as recommended.](https://github.com/0xSplits/splits-oracle/commit/71d6368d62f8ee28043861fc656d16d726261dc8)
