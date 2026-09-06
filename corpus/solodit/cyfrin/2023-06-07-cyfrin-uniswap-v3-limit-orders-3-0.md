---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-3-0
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Use stack variables rather than making repeated external calls
vuln_class: []
---

# Use stack variables rather than making repeated external calls

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

Within `LimitOrderRegistry::withdrawNative`, calls to determine the contract balance of native/wrapped native assets are cached in [stack variables](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L437-L438) but then never used. When performing subsequent transfers, the respective functions are [called again](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L441-L442) to determine the amount to send, wasting gas on repeated external calls as the stack variables could simply be used instead.

**GFX Labs:** Fixed in commit [4cff05a](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/4cff05a1e6acd5f03bac527f0121eb3d3385fc2b).

**Cyfrin:** Acknowledged.
