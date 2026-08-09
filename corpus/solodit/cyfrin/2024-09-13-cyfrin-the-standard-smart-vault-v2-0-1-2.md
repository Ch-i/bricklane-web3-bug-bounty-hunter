---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-09-13-cyfrin-the-standard-smart-vault-v2-0-1-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2024-09-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md
tags:
- firm:cyfrin
- report:2024-09-13-cyfrin-the-standard-smart-vault-v2-0
title: Insufficient validation of Chainlink data feeds
vuln_class: []
---

# Insufficient validation of Chainlink data feeds

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-09-13-cyfrin-the-standard-smart-vault-v2.0.md)_

---

**Description:** `PriceCalculator` is a contract responsible for providing the Chainlink oracle prices for assets used by The Standard. Here, the price for an asset is queried and then normalized to 18 decimals before being returned to the caller:

```solidity
function tokenToUSD(ITokenManager.Token memory _token, uint256 _tokenValue) external view returns (uint256) {
    Chainlink.AggregatorV3Interface tokenUsdClFeed = Chainlink.AggregatorV3Interface(_token.clAddr);
    uint256 scaledCollateral = _tokenValue * 10 ** getTokenScaleDiff(_token.symbol, _token.addr);
    (,int256 _tokenUsdPrice,,,) = tokenUsdClFeed.latestRoundData();
    return scaledCollateral * uint256(_tokenUsdPrice) / 10 ** _token.clDec;
}

function USDToToken(ITokenManager.Token memory _token, uint256 _usdValue) external view returns (uint256) {
    Chainlink.AggregatorV3Interface tokenUsdClFeed = Chainlink.AggregatorV3Interface(_token.clAddr);
    (, int256 tokenUsdPrice,,,) = tokenUsdClFeed.latestRoundData();
    return _usdValue * 10 ** _token.clDec / uint256(tokenUsdPrice) / 10 ** getTokenScaleDiff(_token.symbol, _token.addr);
}
```

However, these calls to `AggregatorV3Interface::latestRoundData` lack the necessary validation for Chainlink data feeds to ensure that the protocol does not ingest stale or incorrect pricing data that could indicate a faulty feed.

**Impact:** Stale prices can result in unnecessary liquidations or the creation of insufficiently collateralised positions.

**Recommended Mitigation:** Implement the following validation:

```diff
-   (,int256 _tokenUsdPrice,,,) = tokenUsdClFeed.latestRoundData();
+   (uint80 _roundId, int256 _tokenUsdPrice, , uint256 _updatedAt, ) = tokenUsdClFeed.latestRoundData();
+   if(_roundId == 0) revert InvalidRoundId();
+   if(_tokenUsdPrice == 0) revert InvalidPrice();
+   if(_updatedAt == 0 || _updatedAt > block.timestamp) revert InvalidUpdate();
+   if(block.timestamp - _updatedAt > TIMEOUT) revert StalePrice();
```

Given the intention to deploy these contracts to Arbitrum, it is also recommended to check the sequencer uptime. The documentation for implementing this is [here](https://docs.chain.link/data-feeds/l2-sequencer-feeds) with a [code example](https://docs.chain.link/data-feeds/l2-sequencer-feeds#example-code).

**The Standard DAO:** Fixed by commit [`8e78f7c`](https://github.com/the-standard/smart-vault/commit/8e78f7c55cc321e789da3d9f6b818ea740b55dc8).

**Cyfrin:** Verified, additional validation of Chainlink price feed data has been added; however, timeouts should be specified on a per-feed basis, and 24 hours is likely too long for most feeds. The sequencer uptime feed has also not been implemented, but this is an important addition. Note that the `hardhat/console.sol` import should be removed from `PriceCalculator.sol`.

**The Standard DAO:** Fixed by commit [`7dfbff1`](https://github.com/the-standard/smart-vault/commit/7dfbff1c6a36b184f71eebcf0763131e53dccfc9).

**Cyfrin:** Verified, additional timeout logic and the sequencer uptime check have been added.

\clearpage
