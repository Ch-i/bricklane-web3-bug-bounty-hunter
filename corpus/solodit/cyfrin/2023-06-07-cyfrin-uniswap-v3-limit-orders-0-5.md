---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-0-5
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Gas griefing denial-of-service on `performUpkeep`
vuln_class: []
---

# Gas griefing denial-of-service on `performUpkeep`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** To mitigate against issues arising from a tangled list, `LimitOrderRegistry::performUpkeep` was modified to continue walking the list toward its head/tail until the next order that matches the walk direction is found. This is achieved using a [while loop](https://github.com/crispymangoes/uniswap-v3-limit-orders/blob/83f5db9cb90926c11ee6ce872dc165b7f600f3d8/src/LimitOrderRegistry.sol#L847); however, this is susceptible to gas griefing attacks if there are a large number of orders with the opposite direction placed between the current and next order. Whilst order spamming is somewhat mitigated by the `minimumAssets` requirement, a reasonably well-funded/anarchic attacker can cause this loop to consume too much gas, greater than the maximum specified gas per upkeep, by placing a series of small orders which could prevent legitimate ITM orders from being fulfilled.

**Impact:** It is possible for a malicious user to perform a denial-of-service attack on upkeep, preventing ITM orders from being fulfilled.

**Recommended Mitigation:** Implement a second order book for orders in the opposite direction, as discussed, removing the need to walk the list until the next order that matches the walk direction is found.

**GFX Labs:** Fixed by separating the order book into two lists, and having orders in opposite directions use completely different LP positions in commits [7b65915](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/7b6591508cc0f412edd7f105f012a0cbb7f4b1fe) and [9e9ceda](https://github.com/crispymangoes/uniswap-v3-limit-orders/commit/9e9cedad083ff9812a9782a88ac9db5cd713b743).

**Cyfrin:** Acknowledged.

\clearpage
