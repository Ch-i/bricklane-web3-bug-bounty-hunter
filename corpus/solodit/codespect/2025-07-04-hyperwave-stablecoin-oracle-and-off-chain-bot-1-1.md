---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-1-1
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[M-02] Incorrectly assumes that the USDE/USDC rate will not exceed 1 most
  of the time'
vuln_class: []
---

# [M-02] Incorrectly assumes that the USDE/USDC rate will not exceed 1 most of the time

_Section severity (from Solodit section header): Medium_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`RedstoneStablecoinRateProvider.sol`](https://github.com/SwellNetwork/boring-vault/tree/ce21e49b7a7be06c3a96c3c3ea6982c32e3ff224/src/oracles/RedstoneStablecoinRateProvider.sol)

**Description:**

The `getRate()` function obtains the price from the Redstone price feed and then calculates the rate, but both the price of USDE and the resulting rate are capped at 1.

```solidity
function _calculateRate(uint256 baseRate, uint256 quoteRate) internal view returns (uint256) {
    //...
    uint256 oneQuoteRate = 10 ** quoteRateDecimals;
    uint256 minQuoteRate = quoteRate > oneQuoteRate ? oneQuoteRate : quoteRate;

    uint256 rate = (minQuoteRate * SCALE) / baseRate;

    return rate > ONE ? ONE : rate;
}
```

The team’s response was:

> In some cases, the price of USDE/USDC can be slightly higher than 1. We don’t want to mint more HLP than necessary, especially since we know that prices will revert to 1 at some point.

However, based on actual observations of the Redstone oracle, the price of USDE remains around 1.0000 to 1.0001 for extended periods, while the price of USDC stays around 0.9997 to 1.0000. For example, the USDE price from June 2nd to June 9th consistently stayed above 1. This means that the USDE/USDC ratio should be greater than 1 under stable conditions, not equal to 1 as the team expects. As a result, the exchange rate is underestimated under normal conditions.

**Impact:** Most of the time, the exchange rate will be lower than the actual rate.

**Recommendation:** Adjust the maximum cap slightly higher.

**Status:** Fixed

**Client response:** Fixed in [PR-6](https://github.com/SwellNetwork/boring-vault/pull/6/files) by adding `MAX_RATE`, which can be changed by the governor.
