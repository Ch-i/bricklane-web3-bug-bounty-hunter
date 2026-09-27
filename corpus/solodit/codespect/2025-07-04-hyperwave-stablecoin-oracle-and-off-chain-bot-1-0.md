---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-1-0
ingested_at: '2026-09-27T10:10:51Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[M-01] Incorrect price validity check'
vuln_class: []
---

# [M-01] Incorrect price validity check

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`RedstoneStablecoinRateProvider.sol`](https://github.com/SwellNetwork/boring-vault/tree/ce21e49b7a7be06c3a96c3c3ea6982c32e3ff224/src/oracles/RedstoneStablecoinRateProvider.sol)

**Description:**

When checking the price validity of the quote token, the code mistakenly uses `MAX_TIME_FROM_LAST_UPDATE_BASE_FEED` instead of `MAX_TIME_FROM_LAST_UPDATE_QUOTE_FEED`.

```solidity
function getRate() public view returns (uint256 rate) {
    //...
    (, int256 _quoteRate,, uint256 lastUpdatedAtQuote,) = PRICE_FEED_QuoteFeed.latestRoundData();

    if (
        lastUpdatedAtQuote > block.timestamp
            || block.timestamp - lastUpdatedAtQuote > MAX_TIME_FROM_LAST_UPDATE_BASE_FEED
    ) {
        revert MaxTimeFromLastUpdatePassed(block.timestamp, lastUpdatedAtQuote);
    }
    //...
}
```

**Impact:** This causes the quote token price validity period to deviate from the expected duration.

**Recommendation:** Use `MAX_TIME_FROM_LAST_UPDATE_QUOTE_FEED` to validate the freshness of the quote token price.

**Status:** Fixed

**Client response:** Fixed in [PR-6](https://github.com/SwellNetwork/boring-vault/pull/6/files).
