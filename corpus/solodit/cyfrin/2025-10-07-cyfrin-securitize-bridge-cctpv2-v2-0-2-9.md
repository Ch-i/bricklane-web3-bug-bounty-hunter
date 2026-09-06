---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Remove unused function `USDCBridgeV2::_redeemUSDC`
vuln_class: []
---

# Remove unused function `USDCBridgeV2::_redeemUSDC`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** The `private` function `USDCBridgeV2::_redeemUSDC` is not used anywhere; remove it.

**Securitize:** Fixed in commit [07a872e](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/07a872e8266411a440b736e328a86528b75cbdb0).

**Cyfrin:** Verified.
