---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-3-2
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Use `targetAddress` instead of `bridgeAddresses[targetChain]` for check in
  `SecuritizeBridge::bridgeDSTokens`
vuln_class: []
---

# Use `targetAddress` instead of `bridgeAddresses[targetChain]` for check in `SecuritizeBridge::bridgeDSTokens`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Use `targetAddress` instead of `bridgeAddresses[targetChain]` for check in `SecuritizeBridge::bridgeDSTokens`:
```diff
        address targetAddress = bridgeAddresses[targetChain];
-       require(bridgeAddresses[targetChain] != address(0), "No bridge address available");
+       require(targetAddress != address(0), "No bridge address available");
```

**Securitize:** Fixed in commit [9081b85](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/9081b858ffddcf1b9b6a3eafcbee3b6a2da192e8).

**Cyfrin:** Verified.
