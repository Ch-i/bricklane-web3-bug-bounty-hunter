---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-5
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: Rename `StrategyPassiveManagerUniswap::price` to `scaledUpPrice` to explicitly
  indicate returned price is scaled up
vuln_class: []
---

# Rename `StrategyPassiveManagerUniswap::price` to `scaledUpPrice` to explicitly indicate returned price is scaled up

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** The current implementation of function `price` returns the price scaled up but the function name doesn't indicate this. Other places in the code that use this function do scale the price down, but the risk is that in the future as the protocol continues to evolve another developer may call the `price` function without realizing the returned price is scaled up and hence won't scale it down.

**Recommended mitigation:**
Rename the function to `scaledUpPrice` such that the function callers are explicitly informed they need to scale it down.

**Beefy:**
Fixed in commit [319cfa0](https://github.com/beefyfinance/experiments/commit/319cfa013263bdab8790bebaa041737e30f52c3b).

**Cyfrin:** Verified.
