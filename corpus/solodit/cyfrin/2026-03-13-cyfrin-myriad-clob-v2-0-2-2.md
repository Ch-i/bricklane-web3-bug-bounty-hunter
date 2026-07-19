---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-13-cyfrin-myriad-clob-v2-0-2-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-13-cyfrin-myriad-clob-v2-0
title: '`FeeModule::setMarketFees` permits 100% fee rates'
vuln_class: []
---

# `FeeModule::setMarketFees` permits 100% fee rates

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-13-cyfrin-myriad-clob-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-13-cyfrin-myriad-clob-v2.0.md)_

---

**Description:** `FeeModule::setMarketFees` validates individual fee rates against `BPS` (10000 basis points = 100%):

```solidity
// FeeModule.sol:102
require(tiers[i].makerFeeBps <= BPS && tiers[i].takerFeeBps <= BPS, "fee too high");
```

This allows the `FEE_ADMIN` to configure a tier with `makerFeeBps = 10000` and `takerFeeBps = 10000`. In a direct match, the seller would receive 0 proceeds and the buyer would pay double the notional value (all sent to fees). Even without malicious intent, misconfigured fee schedules (e.g., entering basis points when percentages are expected) could result in catastrophic fees.

**Recommended Mitigation:** Introduce a protocol-level maximum fee constant and enforce it:

```solidity
uint256 public constant MAX_FEE_BPS = 500; // 5%

require(tiers[i].makerFeeBps <= MAX_FEE_BPS && tiers[i].takerFeeBps <= MAX_FEE_BPS, "fee too high");
```

Make `MAX_FEE_BPS` configurable only by `DEFAULT_ADMIN_ROLE` with a separate governance process.

**Myriad:** Fixed in commit [`e7a85bc`](https://github.com/Polkamarkets/polkamarkets-js/commit/e7a85bccc3fac7d14a2b95cb6eb46b320274c0f7)

**Cyfrin:** Verified. Max fee of 10% (`1000`) enforced.
