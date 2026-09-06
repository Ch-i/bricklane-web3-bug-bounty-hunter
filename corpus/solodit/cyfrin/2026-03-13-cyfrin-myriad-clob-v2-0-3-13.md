---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-3-13
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`FeeModule::_lookupFees` returns zero fees when price is above all configured
  tiers'
vuln_class: []
---

# `FeeModule::_lookupFees` returns zero fees when price is above all configured tiers

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** Tiers are sorted by `maxPrice`, `FeeModule::_lookupFees` walks the tiers and returns the first tier whose `maxPrice` is greater than the trade price. If the price is greater every tier’s `maxPrice`, we fall through and return `(0, 0)`.

When the highest configured tier has `maxPrice` less than `1e18` (ONE), there is a range of valid prices, from that `maxPrice` up to ONE, for which no tier matches. Trades in that range therefore pay zero maker and taker fees.


**Recommended Mitigation:** Because `(0, 0)` is only returned when the price is above all configured tiers, consider introducing a configurable non-zero default for that case. Or a requirement in `FeeModule::setMarketFees` that the last tier’s `maxPrice` equals ONE so that every price in `(0, ONE]` falls into some tier. The former allows a configurable fallback; the latter keeps a single tier structure but ensures full coverage up to ONE.

**Myriad:** **Cyfrin:**

\clearpage
