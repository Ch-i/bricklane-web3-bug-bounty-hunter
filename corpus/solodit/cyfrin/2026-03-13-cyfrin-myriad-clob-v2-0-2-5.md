---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-5
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: Admin void with arbitrary payout ratios allows buy then redeem profit
vuln_class: []
---

# Admin void with arbitrary payout ratios allows buy then redeem profit

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `PredictionMarketV3ManagerCLOB::adminVoidMarket` lets a resolution admin set custom payout ratios `outcome0Payout` and `outcome1Payout` (which must sum to `1e18`) and immediately marks the market resolved. We do not require the market to be closed first, and we do not tie the void payouts to the current market prices. So the admin can void at any time with any valid split, for example 50/50, regardless of the prevailing yes/no ratio in the order book.

If the void payouts differ from the prices at which users can still trade, someone can buy the cheaper outcome and redeem at the void ratio for a risk-free profit. For instance, if YES trades at 60 and NO at 40, and the admin voids with 50/50, a user can front-run this call and buy NO at 40 and directly after voided receive 50 per share on redemption, gaining 10 per share. The same holds in reverse if the void favours the other side. The value of shares therefore jumps at resolution in a way that does not reflect the last tradable prices, and the last movers before the void can capture that gap.

```solidity
// PredictionMarketV3ManagerCLOB.sol:205-220
function adminVoidMarket(
  uint256 marketId,
  uint256 outcome0Payout,
  uint256 outcome1Payout
) external nonReentrant returns (int256) {
  require(registry.hasRole(registry.RESOLUTION_ADMIN_ROLE(), msg.sender), "not resolution admin");
  require(outcome0Payout + outcome1Payout == ONE, "payouts must sum to 1e18");
  // ... no check that market is closed; payouts are arbitrary
  market.resolvedOutcome = -1;
  market.state = MarketState.resolved;
  voidedPayouts[marketId] = [outcome0Payout, outcome1Payout];
```

**Impact:** Users can buy at current market prices and redeem at the admin-chosen void ratios when those ratios differ from market prices, locking in profit. Void resolution can create a step change in share value relative to the last tradable prices, allowing value extraction.

**Recommended Mitigation:** Make voiding a two-step process. In the first step, close the market (e.g. set state to closed or a dedicated “pending void” state) so that no further buys or sells can occur. In the second step, set the void payouts. When setting the payouts, use the current yes/no ratio (e.g. from a snapshot of the order book or the last traded prices at close) so that the void ratios align with the market at the time trading stopped. That avoids stepwise jumps in share value and removes the buy-then-redeem arbitrage.

**Myriad:** Fixed in commit [`4c4ec70`](https://github.com/Polkamarkets/polkamarkets-js/commit/4c4ec70b73cc506249a28b435205e97449cde3c0)

**Cyfrin:** Verified.
