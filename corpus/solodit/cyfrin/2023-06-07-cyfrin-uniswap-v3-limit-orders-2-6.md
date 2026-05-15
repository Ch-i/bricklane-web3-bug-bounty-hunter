---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Re-entrancy in `LimitOrderRegistry::newOrder` means tokens with transfer hooks
  could take over execution to manipulate price to be immediately ITM, bypassing validation
vuln_class: []
---

# Re-entrancy in `LimitOrderRegistry::newOrder` means tokens with transfer hooks could take over execution to manipulate price to be immediately ITM, bypassing validation

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

Whilst there does not appear to be any direct benefit to an attacker, it is possible for tokens with transfer hooks to take over execution from in-flight calls to `LimitOrderRegistry::newOrder`. This function [validates](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L518) that the new order status is OTM prior to performing the [transfer](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L527) of `assetIn` from the caller. An input token such as an ERC-777, which has such transfer hooks, could therefore be used to skew the pool tick after the new order has already passed validation such that it is actually MIXED or ITM. To mitigate against this, consider moving the asset transfer block to before the order is validated OTM, carefully select allowlisted tokens or make `newOrder` non-reentrant.

**GFX Labs:** Fixed in commit [4cff05a](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/4cff05a1e6acd5f03bac527f0121eb3d3385fc2b).

**Cyfrin:** Acknowledged.

\clearpage
