---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2023-06-07-cyfrin-uniswap-v3-limit-orders-1-4
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2023-06-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md
tags:
- firm:cyfrin
- report:2023-06-07-cyfrin-uniswap-v3-limit-orders
title: Fulfillable ITM orders may not always be fulfilled
vuln_class: []
---

# Fulfillable ITM orders may not always be fulfilled

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2023-06-07-cyfrin-uniswap-v3-limit-orders.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2023-06-07-cyfrin-uniswap-v3-limit-orders.md)_

---

**Description:** Currently, orders are only fulfillable via `LimitOrderRegistry::performUpkeep` which processes them
via the doubly linked list, with a limit of `maxFillsPerUpkeep` orders per call. Considering extreme and/or adversarial market conditions, there is no guarantee that all legitimate orders will eventually be processed. If the pool tick varies significantly and rapidly, as is the case for large price swings, and there exist large number of batch orders on the book, greater than `maxFillsPerUpkeep`, then only a subset of orders can be fulfilled in a given block. Assuming the price deviation lasts only a small number of blocks, it is possible that fulfillable ITM orders in the list are not cleared before they once again become OTM.

**Impact:** Valid and fulfillable ITM orders may not be fulfilled even though their liquidity within the position is technically being used for the duration the pool tick exceeds their target tick price.

**Recommended Mitigation:** To guarantee that any order can be fulfilled, consider adding a public `fulfillOrder` function that can be called by any user to fulfil a specific order independently from its position in the list. The order can be simply fulfilled and removed from the list, without affecting the upkeep procedure.

**GFX Labs:** Acknowledged. Even in traditional market settings, price can go past some limit order trigger, but that order can still be unfilled, if there is not enough volume.

Adding a custom function to allow users to fulfill a specific order is a possible solution, but its only a solution if the users create some bot which is better at TX management than Chainlink Automation, and that is a big ask for users. Because of this, the function was not added to reduce contract size.

**Cyfrin:** Acknowledged.

\clearpage
