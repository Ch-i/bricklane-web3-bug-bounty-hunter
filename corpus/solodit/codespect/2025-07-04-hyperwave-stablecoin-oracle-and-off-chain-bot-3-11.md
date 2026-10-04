---
affected_contracts: []
derives_from: []
id: solodit-codespect-2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot-3-11
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md
tags:
- firm:codespect
- report:2025-07-04-hyperwave-stablecoin-oracle-and-off-chain-bot
title: '[I-12] Validity checks after price type conversion may fail to throw the expected
  error'
vuln_class: []
---

# [I-12] Validity checks after price type conversion may fail to throw the expected error

_Section severity (from Solodit section header): Informational_  
_Audit firm: CODESPECT_  
_Source report: [2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md](https://github.com/solodit/solodit_content/blob/main/reports/CODESPECT/2025-07-04-Hyperwave-Stablecoin-Oracle-and-Off-Chain-Bot.md)_

---

**Files:** [`RedstoneStablecoinRateProvider.sol`](https://github.com/SwellNetwork/boring-vault/tree/ce21e49b7a7be06c3a96c3c3ea6982c32e3ff224/src/oracles/RedstoneStablecoinRateProvider.sol)

**Description:**

After fetching the price from the oracle, the price is first converted from `int256` to `uint256`, and only then is the `price > 0` check performed.

```solidity
function getRate() public view returns (uint256 rate) {
    //...
    rate = _calculateRate(_baseRate.toUint256(), _quoteRate.toUint256());

    _rateCheck(rate);
}

function _calculateRate(uint256 baseRate, uint256 quoteRate) internal view returns (uint256) {
    require(baseRate > 0, "Base rate must be greater than 0");
    require(quoteRate > 0, "Quote rate must be greater than 0");
    //...
}
```

Under the current integration with the Redstone oracle, this step poses no issue because Redstone includes an internal `price > 0` check when publishing prices.

However, in the future, the project may reuse with Chainlink. Chainlink may return a negative price in the event of an oracle failure. As a result, converting from `int256` to `uint256` before performing the `price > 0` check could directly trigger a `SafeCastOverflowedIntToUint` error, instead of the intended custom or expected error.

**Impact:** The protocol fails to throw the expected error in the event of an abnormal price.

**Recommendation:** It is recommended to check `price > 0` before performing the type conversion.

**Status:** Fixed

**Client response:** Fixed in [PR-6](https://github.com/SwellNetwork/boring-vault/pull/6/files).
