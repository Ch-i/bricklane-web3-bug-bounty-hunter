---
affected_contracts: []
derives_from: []
id: solodit-codespect-2024-12-10-redstone-oracles-0-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2024-12-10T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md
tags:
- firm:codespect
- report:2024-12-10-redstone-oracles
title: '[M-01] Potential Scaling to Unexpected Decimal Places'
vuln_class: []
---

# [M-01] Potential Scaling to Unexpected Decimal Places

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2024-12-10-RedStone-Oracles.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2024-12-10-RedStone-Oracles.md)_

---

**Files:** [MultiFeedAdapterWithoutRounds.sol](https://github.com/redstone-finance/redstone-oracles-monorepo/blob/ff0f3dcb085f28bd80ddc096825701db6e14d0af/packages/on-chain-relayer/contracts/price-feeds/without-rounds/MultiFeedAdapterWithoutRounds.sol#L231-L232)

**Description:**

The `MultiFeedAdapterWithoutRounds` contract allows updates and price retrieval for multiple feeds. One way to obtain an asset’s price is through the `priceOf(...)` function, which accepts the asset’s address as input:

```solidity
function priceOf(address asset) public view virtual returns (uint256) {
    bytes32 dataFeedId = getDataFeedIdForAsset(asset);
    uint256 latestValue = getValueForDataFeed(dataFeedId);
    return convertDecimals(dataFeedId, latestValue);
}
```

This function retrieves the data feed ID using the asset address, gets the latest price, and then scales it to 10^18 decimals using:

```solidity
function convertDecimals(bytes32 /* dataFeedId */, uint256 valueFromRedstonePayload) public view virtual returns (uint256) {
    // @audit-issue Missing address(dataFeed).decimals() and proper scaling to reflect correct decimals
    return valueFromRedstonePayload * DEFAULT_DECIMAL_SCALER_LAYERBANK;
}
```

The issue is that the price is always multiplied by 10^10, assuming a default of 10^8 decimals from the `PriceFeed`. However, the function does not consider the actual decimals of the specific data feed. This could lead to a mismatch where the smart contract receives a price in a different decimal format than expected, potentially causing incorrect calculations.

**Recommendation:** Incorporate the data feed’s `decimals()` function to adjust the scaling based on the returned value dynamically.

**Status:** Acknowledged

**Client response:** We’ve assumed we’ll override the `convertDecimals` function fo such cases. In practice, this LayerBank interface is in use only by one project and we’ll probably remove it in future.
