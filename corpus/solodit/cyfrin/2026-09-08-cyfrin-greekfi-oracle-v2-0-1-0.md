---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-oracle-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-oracle-v2-0
title: '`DeployMorphoVault` sets the ETH feed max age equal to its heartbeat, so `OracleReceipt::price`
  reverts for a short window after most rounds'
vuln_class: []
---

# `DeployMorphoVault` sets the ETH feed max age equal to its heartbeat, so `OracleReceipt::price` reverts for a short window after most rounds

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-oracle-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-oracle-v2.0.md)_

---

**Description:** `DeployMorphoVault` wires `ChainlinkCrossPriceSource` with `UNDERLYING_MAX_AGE = 3600` for the ETH/USD feed, and the comment describes the value as "heartbeat + grace":

```solidity
address constant ETH_USD_FEED = 0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419;
address constant SUSDE_USD_FEED = 0xFF3BC18cCBd5999CE63E788A1c250a88626aD099;
uint256 constant UNDERLYING_MAX_AGE = 3600; // heartbeat + grace
uint256 constant CASH_MAX_AGE = 90000; // 25h
```

```solidity
ChainlinkCrossPriceSource source = new ChainlinkCrossPriceSource(
    AggregatorV3Interface(ETH_USD_FEED), AggregatorV3Interface(SUSDE_USD_FEED), UNDERLYING_MAX_AGE, CASH_MAX_AGE
);
```

3600 s is exactly the ETH/USD heartbeat, with no grace. Chainlink's heartbeat round lands a few seconds late in calm markets, and `ChainlinkCrossPriceSource::_read` rejects any answer older than `maxAge` with a strict comparison:

```solidity
function _read(AggregatorV3Interface feed, uint256 maxAge) internal view returns (uint256) {
    (, int256 answer,, uint256 updatedAt,) = feed.latestRoundData();
    if (answer <= 0) revert InvalidPrice(address(feed));
    if (updatedAt == 0 || updatedAt > block.timestamp || block.timestamp - updatedAt > maxAge) {
        revert StalePrice(address(feed));
    }
    return uint256(answer);
}
```

Sampled on mainnet on 2026-09-01 from the live aggregator behind the ETH/USD proxy (rounds 33173 to 33193): 11 of the last 20 inter-round gaps were 3612 to 3636 s. During the 12 to 36 s after each such round `block.timestamp - updatedAt > 3600` holds and every `price()` call reverts `StalePrice`. The sUSDe/USD leg is configured correctly (24 h heartbeat, 25 h max age).

**Impact:** Morpho `borrow`, `liquidate`, and debt-side `withdrawCollateral` revert for a 12-36 second window after most ETH/USD heartbeat rounds.

**Recommended Mitigation:** Set the underlying max age to the heartbeat plus a real grace period and make the comment true, for example:

```solidity
uint256 constant UNDERLYING_MAX_AGE = 3600 + 600; // heartbeat + grace
```

Chainlink's guidance is to allow a margin above the heartbeat. A value of 3900 to 4200 s keeps the staleness guard meaningful without tripping on ordinary round latency.

**GreekFi:** Fixed in [PR40](https://github.com/greekfi/contracts/pull/40)

**Cyfrin:** Verified. The deployment script now allows a ten-minute grace period above the ETH/USD feed heartbeat.

\clearpage
