---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-07-cyfrin-suzaku-core-v2-0-2-9
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-07-07T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-07-cyfrin-suzaku-core-v2-0
title: Unbounded weight scale factor causes precision loss in stake conversion, potentially
  leading to loss of operator funds
vuln_class: []
---

# Unbounded weight scale factor causes precision loss in stake conversion, potentially leading to loss of operator funds

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-07-cyfrin-suzaku-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-07-cyfrin-suzaku-core-v2.0.md)_

---

**Description:** The `AvalancheL1Middleware` uses a `WEIGHT_SCALE_FACTOR` to convert between 256-bit stake amounts and 64-bit validator weights for the P-Chain. However, there are no bounds on this scale factor, and an inappropriately high value can cause precision loss.

The conversion process works as follows:

`stakeToWeight(): weight = stakeAmount / scaleFactor`
`weightToStake(): recoveredStake = weight * scaleFactor`

When `WEIGHT_SCALE_FACTOR` is too high relative to stake amounts, the division in `stakeToWeight()` truncates to zero, making the stake effectively unusable.


**Impact:** Weight recorded for validator can be 0 due to precision loss.

**Recommended Mitigation:** Consider implementing reasonable maximum bounds in the constructor.

**Suzaku:**
Fixed in commit [b38dfed](https://github.com/suzaku-network/suzaku-core/pull/155/commits/b38dfed1d21a628582b11d217f5112290b973034).

**Cyfrin:** Verified.
