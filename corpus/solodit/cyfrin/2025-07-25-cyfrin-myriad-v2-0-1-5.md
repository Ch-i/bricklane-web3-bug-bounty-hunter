---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-25-cyfrin-myriad-v2-0-1-5
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-25-cyfrin-myriad-v2-0
title: Unused field `MarketResolution.resolved`
vuln_class: []
---

# Unused field `MarketResolution.resolved`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-25-cyfrin-myriad-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-25-cyfrin-myriad-v2.0.md)_

---

**Description:** The `MarketResolution` struct includes a [`resolved`](http://github.com/Polkamarkets/polkamarkets-js/blob/24f1394be94d27433d2e3a7370442126e1c1e5ba/contracts/PredictionMarketV3_4.sol#L160) field, but it is not used anywhere in the current contract logic. Keeping unused state variables increases code complexity and may confuse future maintainers or auditors. It may also suggest incomplete or outdated logic.

Consider either removing the `resolved` field if it is unnecessary, or integrate it meaningfully into the resolution logic if it was intended to serve a functional purpose.

**Myriad:** Fixed in [PR#81](https://github.com/Polkamarkets/polkamarkets-js/pull/81), commit [`6060137`](https://github.com/Polkamarkets/polkamarkets-js/pull/81/commits/60601378ab213819e79836c4cec3533fe3c649b3)

**Cyfrin:** Verified. `resolved` removed from the `MarketResolution` struct.
