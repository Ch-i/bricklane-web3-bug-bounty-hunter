---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-01-cyfrin-licredity-v2-0-4-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-09-01T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-01-cyfrin-licredity-v2-0
title: Wrong short-circuit logic in Chainlink oracle update
vuln_class: []
---

# Wrong short-circuit logic in Chainlink oracle update

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-01-cyfrin-licredity-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-01-cyfrin-licredity-v2.0.md)_

---

**Description:** The `ChainlinkOracle::update` function attempts to short-circuit (skip) updates if neither the price nor the timestamp has changed by checking:
```solidity
if (sqrtPriceX96 == lastPriceX96 && currentTimeStamp == block.timestamp) {
    return;
}
```
However, this logic is flawed because `sqrtPriceX96` is the square root price from Uniswap V4, while `lastPriceX96` is calculated as `(sqrtPriceX96^2) >> 96` (i.e., the actual price, not the square root). As a result, `sqrtPriceX96 == lastPriceX96` will almost never be true, except in trivial cases (e.g., both are zero). This means the short-circuit will almost never trigger, and the function will perform unnecessary calculations on every call.

**Impact:** Inefficient execution: The function will always proceed with the update logic, even when no update is needed, leading to unnecessary gas consumption.

**Recommended Mitigation:** Change the short-circuit condition to compare `sqrtPriceX96` with its previous value (store the last `sqrtPriceX96`), or compare the correctly calculated price values:

```solidity
uint256 priceX96 = (uint256(sqrtPriceX96) * uint256(sqrtPriceX96)) >> 96;
if (priceX96 == lastPriceX96 && currentTimeStamp == block.timestamp) {
    return;
}
```

Alternatively, remove the short-circuit logic from the `update` function.

**Licredity:** Fixed in [PR#14](https://github.com/Licredity/licredity-v1-oracle/pull/14/files), commit [`13e2cb0`](https://github.com/Licredity/licredity-v1-oracle/commit/13e2cb0f7174bf8d51d71f06012bfc6661727840)

**Cyfrin:** Verified. `sqrtPriceX86` is now calculated before the comparison and used in the same.
