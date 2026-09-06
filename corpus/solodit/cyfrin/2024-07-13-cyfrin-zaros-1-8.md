---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: '`TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` uses incorrect
  price during order settlement'
vuln_class: []
---

# `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` uses incorrect price during order settlement

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** During order settlement `SettlementBranch::_fillOrder` uses an off-chain price provided by the keeper:

```solidity
File: SettlementBranch.sol
120:         ctx.fillPrice = perpMarket.getMarkPrice(
121:             ctx.sizeDelta, settlementConfiguration.verifyOffchainPrice(priceData, ctx.sizeDelta.gt(SD_ZERO))
122:         );
123:
124:         ctx.fundingRate = perpMarket.getCurrentFundingRate();
125:         ctx.fundingFeePerUnit = perpMarket.getNextFundingFeePerUnit(ctx.fundingRate, ctx.fillPrice);
```

All variables including `ctx.fillPrice` and `ctx.fundingFeePerUnit` are calculated based on this price.

But during the margin requirement validation in `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` the price input provided by the keeper is not used, instead this uses an index price:

```solidity
File: TradingAccount.sol
207:             UD60x18 markPrice = perpMarket.getMarkPrice(sizeDeltaX18, perpMarket.getIndexPrice());
208:             SD59x18 fundingFeePerUnit =
209:                 perpMarket.getNextFundingFeePerUnit(perpMarket.getCurrentFundingRate(), markPrice);
```

**Impact:** All calculations in `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` may be incorrect as the price provided by the keeper may differ from the current index price. Hence during an order settlement `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` may return incorrect outputs.

**Recommended Mitigation:** During order settlement `TradingAccount::getAccountMarginRequirementUsdAndUnrealizedPnlUsd` should use the same off-chain price for `targetMarketId` provided by the keeper.

**Zaros:** Acknowledged; this is something we will refactor in V2. In practice the difference is negligible; in the "worst-case" scenario what could happen is that an order would be filled even though the user was slightly under the initial margin requirement. While not desirable, the user would not be subject to immediate liquidation as that occurs at the maintenance margin, so the impact here appears very minimal.
