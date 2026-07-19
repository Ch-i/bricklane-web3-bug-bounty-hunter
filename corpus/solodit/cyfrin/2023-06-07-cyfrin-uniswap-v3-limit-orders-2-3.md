---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Limit orders can be frozen for one side of a Uniswap v3 pool if `minimumAssets`
  has not been set for one of the tokens
vuln_class: []
---

# Limit orders can be frozen for one side of a Uniswap v3 pool if `minimumAssets` has not been set for one of the tokens

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

To prevent spamming low liquidity orders, `LimitOrderRegistry::minimumAssets` must be set for a given asset before limit orders are allowed to be placed. A Uniswap v3 pool contains two assets, but `LimitOrderRegistry::setMinimumAssets` is called for a specific asset across the entire contract and is not pool-specific. If this function is not called for both assets in a given pool then limit orders in a given direction will not be allowed, depending on which asset has no minimum set.

**GFX Labs:** Acknowledged. It is in the owner's best interest to make sure both assets in a pool are supported, so that there are more limit orders, and more swap fees generated.

**Cyfrin:** Acknowledged.
