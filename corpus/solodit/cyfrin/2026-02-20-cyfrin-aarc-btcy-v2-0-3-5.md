---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-3-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Cache storage to avoid identical storage reads
vuln_class: []
---

# Cache storage to avoid identical storage reads

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** Reading from storage is expensive; cache storage to avoid identical storage reads:
```solidity
DepositWithdraw.sol
// cache `_treasury` in `withdraw`
142:        require(msg.sender == _treasury, NotAuthorized());
147:        IERC20(token).safeTransferFrom(_treasury, user, amount);

Pricer.sol
// cache `$.priceFeed` in `getPrice, getPriceInfo, getPriceInfos`
159:        require(address($.priceFeed) != address(0), PriceFeedNotSet());
161:        (, int256 answer,, uint256 updatedAt,) = $.priceFeed.getRoundData(uint80(priceId));

182:        require(address($.priceFeed) != address(0), PriceFeedNotSet());
184:        (, int256 answer,, uint256 updatedAt,) = $.priceFeed.getRoundData(uint80(priceId));

205:        require(address($.priceFeed) != address(0), PriceFeedNotSet());
211:            (, int256 answer,, uint256 updatedAt,) = $.priceFeed.getRoundData(uint80(_priceIds[i]));

231:        require(address($.priceFeed) != address(0), PriceFeedNotSet());
233:        (, int256 answer,, uint256 updatedAt,) = $.priceFeed.latestRoundData();

// cache `$.latestPriceId` in `addPrice`, then pass cached value as input to `_addPrice`
// and use that instead of re-reading known value from storage. Same fix in `addCurrentPrice`
261:        if ($.latestPriceId != 0) {
262:            uint256 prev = $.prices[$.latestPriceId].price;
293:        if ($.latestPriceId == 0 || timestamp > $.prices[$.latestPriceId].timestamp) {

351:        if ($.latestPriceId != 0) {
352:            uint256 prev = $.prices[$.latestPriceId].price;

// cache `$.prices[priceId].price` before `if` check and used cache value in `if` check
311:        if ($.prices[priceId].price == 0) {
314:        uint256 oldPrice = $.prices[priceId].price;
```

**Aarc:** Fixed in commit [7c57344](https://github.com/aarc-xyz/btcy-contracts-main/commit/7c5734490d875abef38934198e19af81df0ac153).

**Cyfrin:** Verified.
