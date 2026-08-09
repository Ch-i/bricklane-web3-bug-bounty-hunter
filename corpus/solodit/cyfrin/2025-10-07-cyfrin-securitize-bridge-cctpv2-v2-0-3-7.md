---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-7
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Remove unused return from `USDCBridgeV2:_sendUSDCWithPayloadToEvm`
vuln_class: []
---

# Remove unused return from `USDCBridgeV2:_sendUSDCWithPayloadToEvm`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Function `USDCBridgeV2::_sendUSDCWithPayloadToEvm()` returns the sequence number from the `wormholeRelayer.sendToEvm` external call. However, this value is never utilized thereafter.

**Recommended Mitigation:** Consider removing this variable.

**Securitize:** Acknowledged.
