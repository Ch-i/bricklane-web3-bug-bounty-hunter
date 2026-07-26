---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1-3-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-07-23T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md
tags:
- firm:cyfrin
- report:2025-07-23-cyfrin-securitize-onofframp-bridge-v2-1
title: The `swap` function emits incorrect event type for existing investor purchases
vuln_class: []
---

# The `swap` function emits incorrect event type for existing investor purchases

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-23-cyfrin-securitize-onofframp-bridge-v2.1.md)_

---

**Description:** The `SecuritizeOnRamp::swap` function emits a `Swap` event instead of the expected `Buy` event when existing investors purchase assets. According to the interface documentation, the `Swap` event is intended for "new subscription agreements" while the `Buy` event should be emitted "when an existing investor buy assets".
The `swap` function is specifically designed for existing registered investors (enforced by the `investorExists` modifier) to purchase additional assets, making it semantically a "buy" operation rather than a "swap" operation.

**Impact:** Off-chain systems and event listeners may incorrectly categorize existing investor purchases as new subscription agreements, leading to inaccurate tracking and reporting of investor activities.

**Recommended Mitigation:** Replace the `Swap` event emission with the appropriate `Buy` event in the `swap` function:

```diff
- emit Swap(_msgSender(), dsTokenAmount, _liquidityAmount, _msgSender());
+ emit Buy(_msgSender(), _liquidityAmount, dsTokenAmount, navProvider.rate());
```

**Securitize:** Fixed in [2b6c3a](https://github.com/securitize-io/bc-on-off-ramp-sc/commit/2b6c3a8efdc23b4e2fc5fed273987830fbeaee18). Buy event was deprecated and deleted.

**Cyfrin:** Verified.
