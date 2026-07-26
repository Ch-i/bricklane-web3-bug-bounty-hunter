---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-14
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Pending/re-executable messages sourced from old bridge addresses will not be
  executable if bridge address is updated
vuln_class: []
---

# Pending/re-executable messages sourced from old bridge addresses will not be executable if bridge address is updated

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** SecuritizeBridge and USDCBridgeV2 provide owner with the ability to update bridge addresses. This can be done incase a new bridge address is expected to be used and the previous one is being deprecated.

```solidity
function setBridgeAddress(uint16 chainId, address bridgeAddress) external override onlyOwner {
        bridgeAddresses[chainId] = bridgeAddress;
        emit BridgeAddressAdd(chainId, bridgeAddress);
    }
```

**Impact:** One important behaviour to be aware of here is that there could be pending or failed destination messages waiting to be delivered. If the bridge address is updated before these are executed, it is possible for them to never be executable again unless the bridge address is updated to the previous one.

**Recommended Mitigation:** Consider waiting for delivery of pending messages and execute any failed destination messages before updating the bridge address for a chain.

**Securitize:** Acknowledged.

\clearpage
