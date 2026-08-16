---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-17-cyfrin-octodefi-v2-0-1-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-07-17T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-17-cyfrin-octodefi-v2-0
title: Missing staleness check in `PriceOracle::getTokenPrice`
vuln_class: []
---

# Missing staleness check in `PriceOracle::getTokenPrice`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-17-cyfrin-octodefi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-17-cyfrin-octodefi-v2.0.md)_

---

**Description:** `PriceOracle.getTokenPrice()` relays `pythOracle.getPriceUnsafe()` but never verifies the price **publish time** or confidence interval. A price that is hours old (or intentionally frozen) is accepted as fresh.

```solidity
function getTokenPrice(address _token) external view returns (uint256) {
    bytes32 _oracleID = oracleIDs[_token];

    if (_oracleID == bytes32(0)) {
        revert OracleNotExist(_token);
    }

    PythStructs.Price memory price = pythOracle.getPriceUnsafe(_oracleID);

    return _scalePythPrice(price.price, price.expo);
}
```

**Impact:** * Automation fees may be computed from obsolete data, letting attackers over- or under-pay.

**Recommended Mitigation:** Consider using the [getPriceNoOlderThan](https://api-reference.pyth.network/price-feeds/evm/getPriceNoOlderThan) function instead of [getPriceUnsafe](https://api-reference.pyth.network/price-feeds/evm/getPriceUnsafe).

**OctoDeFi:** Fixed in PR [\#24](https://github.com/octodefi/strategy-builder-plugin/pull/24).

**Cyfrin:** Verified. When the oracle reports prices older than 120 seconds, `PriceOracle` will return 0 such that the minimum fee will be used. This is a good solution, although a 0 price will cause panic revert due to division by zero in `calculateTokenAmount()`.

**OctoDeFi:** Fixed in PR [\#27](https://github.com/octodefi/strategy-builder-plugin/pull/27).

**Cyfrin:** Verified. The 0 price case is now explicitly handled to avoid reverting and the threshold has been reduced to 60 seconds. It is possible that this threshold could be too restrictive for specific feeds, and it is recommended to be configured on a per-feed basis.

**OctoDeFi:** Regarding the threshold, we also believe that 60 seconds is quite restrictive, especially considering this is a fee calculation and not a vault with collateral at risk.

Most Pyth oracles update roughly every 1–2 seconds for major tokens. However, it's important to note that these are pull-based oracles, so smaller or less liquid tokens could have much slower update rates.

It might actually make sense to set the threshold much higher to really detect when an oracle is no longer functioning, rather than simply outdated. In any case, we can't fully prevent price manipulation through a single threshold alone.

**Cyfrin:** Acknowledged.
