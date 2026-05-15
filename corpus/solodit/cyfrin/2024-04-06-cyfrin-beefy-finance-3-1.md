---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-04-06-cyfrin-beefy-finance-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-04-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md
tags:
- firm:cyfrin
- report:2024-04-06-cyfrin-beefy-finance
title: '`StrategyPassiveManagerUniswap::twapInterval` should be `uint32`'
vuln_class: []
---

# `StrategyPassiveManagerUniswap::twapInterval` should be `uint32`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-04-06-cyfrin-beefy-finance.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-04-06-cyfrin-beefy-finance.md)_

---

**Description:** Given that `twapInterval` corresponds to a time interval it makes better sense to define it to as `uint32`, avoiding possible wrong assignment through `setTwapInterval` which can affect behavior of `twap()`.

**Beefy:**
Fixed in commit [b520517](https://github.com/beefyfinance/experiments/commit/b520517486fa88da062116f6327ee938dd0b4fb4).

**Cyfrin:** Verified.
