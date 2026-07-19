---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-1
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
title: Use named mapping parameters to make explicit the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to make explicit the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Use named mapping parameters to make explicit the purpose of keys and values:
```solidity
wormhole/WormholeCCTPUpgradeable.sol
79:    mapping(uint16 => uint32) public chainIdToCCTPDomain;

bridge/USDCBridgeV2.sol
63:    mapping(uint16 => address) public bridgeAddresses;
64:    mapping(uint16 => uint32) public chainIdToCCTPDomain;

bridge/SecuritizeBridge.sol
40:    mapping(uint16 => address) public bridgeAddresses;
```

**Securitize:** Fixed in commit [40f4db0](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/40f4db07a0351b3aebb3547a49236a1ca54a99d3).

**Cyfrin:** Verified.
