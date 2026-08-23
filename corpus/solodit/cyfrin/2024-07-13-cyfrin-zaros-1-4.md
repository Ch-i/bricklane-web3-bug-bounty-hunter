---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-1-4
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: Anyone can cancel traders' market orders due to missing access control in `OrderBranch::cancelMarketOrder`
vuln_class: []
---

# Anyone can cancel traders' market orders due to missing access control in `OrderBranch::cancelMarketOrder`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** Anyone can cancel traders' market orders due to missing access control in `OrderBranch::cancelMarketOrder`:

```solidity
function cancelMarketOrder(uint128 tradingAccountId) external {
    MarketOrder.Data storage marketOrder = MarketOrder.loadExisting(tradingAccountId);

    marketOrder.clear();

    emit LogCancelMarketOrder(msg.sender, tradingAccountId);
}
```

**Impact:** Anyone can cancel traders' market orders.

**Recommended Mitigation:** `OrderBranch::cancelMarketOrder` should check if the caller is an owner of the trading account.

```diff
    function cancelMarketOrder(uint128 tradingAccountId) external {
+       TradingAccount.loadExistingAccountAndVerifySender(tradingAccountId);

        MarketOrder.Data storage marketOrder = MarketOrder.loadExisting(tradingAccountId);

        marketOrder.clear();

        emit LogCancelMarketOrder(msg.sender, tradingAccountId);
    }
```

**Zaros:** Fixed in commit [d37c37a](https://github.com/zaros-labs/zaros-core/commit/d37c37abab40bfa2320c6925c359faa501577eb3).

**Cyfrin:** Verified.
