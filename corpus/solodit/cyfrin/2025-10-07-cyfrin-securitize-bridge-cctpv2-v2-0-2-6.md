---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Upgradeable contracts should call `_disableInitializers` in constructor
vuln_class: []
---

# Upgradeable contracts should call `_disableInitializers` in constructor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Upgradeable contracts should [call](https://docs.openzeppelin.com/upgrades-plugins/writing-upgradeable#initializing_the_implementation_contract) `_disableInitializers` in constructor:
```solidity
/// @custom:oz-upgrades-unsafe-allow constructor
constructor() {
    _disableInitializers();
}
```

Affected contracts:
* `SecuritizeBridge`
* `USDCBridgeV2`

**Securitize:** Fixed in commit [4b7f654](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/4b7f654e98b0a2b4d953101372b360c906459d9b).

**Cyfrin:** Verified.
