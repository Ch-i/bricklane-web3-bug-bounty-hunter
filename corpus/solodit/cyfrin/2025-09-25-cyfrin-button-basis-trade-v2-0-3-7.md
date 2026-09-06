---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-25-cyfrin-button-basis-trade-v2-0-3-7
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-09-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-25-cyfrin-button-basis-trade-v2-0
title: '`BasisTradeVault::totalAssets` may undercount pocket-held funds'
vuln_class: []
---

# `BasisTradeVault::totalAssets` may undercount pocket-held funds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-25-cyfrin-button-basis-trade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-25-cyfrin-button-basis-trade-v2.0.md)_

---

**Description:** [`BasisTradeVault::totalAssets`](https://github.com/buttonxyz/button-protocol/blob/9002f2b0d05ba80039bd942c809dbe5bc1a252c9/src/BasisTradeVault.sol#L252-L283) currently depends on the (not-yet-finalized) oracle to report the Pocket’s balance. The oracle may miss pocket-held funds  by excluding assets sitting in the Pocket, which can skew previews and caps. While this can be considered the oracle’s responsibility, consider ensuring `totalAssets()` includes Pocket-held assets, either by including them  explicitly: `IERC20(asset()).balanceOf(pocket)` or by making sure the development of the oracle will include them.

**Button:** Fixed in [`9cde24c`](https://github.com/buttonxyz/button-protocol/commit/9cde24caa4b3f5f37a059bb2fde172cfa374d3a9). Moved to a PPS based oracle.

**Cyfrin:** Verified. The oracle now just returns a price-per-share, which is used to determine the total assets.
