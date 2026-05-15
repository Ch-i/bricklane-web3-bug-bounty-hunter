---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-8
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Missing event for important state changes
vuln_class: []
---

# Missing event for important state changes

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The following calls doesn't emit any events:
* [`LandFactory::updateLockAmount`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/LandFactory.sol#L205-L210)
* [`PredictionMarketV3_4::withdraw`](https://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L1458-L1460)

Events enable off-chain tracking, auditing and transparency. Consider emitting events from the calls above.

**Myriad:** Fixed in [PR#87](https://github.com/Polkamarkets/polkamarkets-js/pull/87), commits [`b40b740`](https://github.com/Polkamarkets/polkamarkets-js/pull/87/commits/b40b7403b227f6e40de984f4d0ff4c3170d6129b) and [`52bdf82`](https://github.com/Polkamarkets/polkamarkets-js/pull/87/commits/52bdf82088a71f721f31c9eeb1da0a79407af5d9)

**Cyfrin:** Verified. Both calls now emit events.

\clearpage
