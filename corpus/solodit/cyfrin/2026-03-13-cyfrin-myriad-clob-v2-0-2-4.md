---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`FeeModule::_lookupFees` returns zero fees at price = 1e18 due to strict less-than
  comparison'
vuln_class: []
---

# `FeeModule::_lookupFees` returns zero fees at price = 1e18 due to strict less-than comparison

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `FeeModule::_lookupFees` uses a strict less-than comparison (`price < tiers[i].maxPrice`) to find the applicable fee tier. Since `maxPrice` is validated as `<= 1e18` (i.e., the maximum tier boundary is 1e18), a trade at exactly `price = 1e18` will not match any tier and fall through to the default `return (0, 0)`.

A price of 1e18 represents a 100% probability outcome — while uncommon, it is explicitly allowed by `_matchOrders` which validates `maker.price <= ONE && taker.price <= ONE`.

```solidity
// FeeModule.sol:151-158
function _lookupFees(uint256 marketId, uint256 price) internal view returns (uint16 makerBps, uint16 takerBps) {
    FeeTier[] storage tiers = _marketFees[marketId];
    for (uint256 i = 0; i < tiers.length; i++) {
        if (price < tiers[i].maxPrice) {  // @audit strict less-than: price=1e18 never matches
            return (uint16(tiers[i].makerFeeBps), uint16(tiers[i].takerFeeBps));
        }
    }
    return (0, 0); // price=1e18 falls through to zero fees
}
```

**Impact:** Trades at `price = 1e18` pay zero fees when the fee admin intended them to be covered by the highest tier. This represents fee revenue leakage.

**Recommended Mitigation:** Change to less-than-or-equal:

```solidity
if (price <= tiers[i].maxPrice) {
```

**Myriad:** Fixed in commit [`8074df6`](https://github.com/Polkamarkets/polkamarkets-js/commit/8074df65a4b3b18b5393eba526621d0c65c96823)

**Cyfrin:** Verified.
