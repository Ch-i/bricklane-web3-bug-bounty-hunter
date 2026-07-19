---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-7
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Use `addressNotZero` modifier on `USDCBridgeV2::setBridgeAddress`
vuln_class: []
---

# Use `addressNotZero` modifier on `USDCBridgeV2::setBridgeAddress`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Use `addressNotZero` modifier on `USDCBridgeV2::setBridgeAddress`:
```diff
-   function setBridgeAddress(uint16 _chainId, address _bridgeAddress) external override onlyRole(DEFAULT_ADMIN_ROLE) {
+   function setBridgeAddress(uint16 _chainId, address _bridgeAddress) external override addressNotZero(_bridgeAddress) onlyRole(DEFAULT_ADMIN_ROLE) {
```

**Securitize:** Fixed in commit [f51d885](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/f51d885e50218167a7fb16d0152337bf8e8445d6).

**Cyfrin:** Verified.
