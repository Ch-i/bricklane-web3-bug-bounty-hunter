---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-2
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
title: Consider enforcing a min TWAP interval in `StrategyPassiveManagerUniswap::setTwapInterval`
  to avoid dangerous assignment
vuln_class: []
---

# Consider enforcing a min TWAP interval in `StrategyPassiveManagerUniswap::setTwapInterval` to avoid dangerous assignment

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** The way TWAP oracle works in UniswapV3 is:

$$tickCumulative(pool,time_{A},time_{B}) = \sum_{i=time_{A}}^{time_{B}} Price_{i}(pool)$$

$$TWAP(pool,time_{A},time_{B}) = \frac{tickCumulative(pool,time_{A},time_{B})}{time_{B} - time_{A}}$$

In this way, if $time_{B} - time_{A}$ is too low it would be relatively easy to manipulate TWAP output. Since $time_{B} - time_{A}$ is represented by `twapInterval`, it would be better to enforce a min value, for instance 5 minutes (consider that current Ethereum blocks emission rate is around 12 seconds).

**Beefy:**
Fixed in commit [b5769c4](https://github.com/beefyfinance/experiments/commit/b5769c4ccad6357ac9d3de2c682749bbaeeae6d1).

**Cyfrin:** Verified.
