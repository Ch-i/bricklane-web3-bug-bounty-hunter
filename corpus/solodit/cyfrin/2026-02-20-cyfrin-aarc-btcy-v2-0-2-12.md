---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-12
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Fee on transfer tokens not supported
vuln_class: []
---

# Fee on transfer tokens not supported

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** The protocol has asked us to examine whether fee on transfer tokens would work with this protocol; currently they are not supported.

However the currently intended token list is WBTC (BitGo), BBTC (Binance), tBTC (Threshold), cbBTC (Coinbase) which don't have a fee on transfer so there is no impact with the intended token list.

**Aarc:** Acknowledged.
