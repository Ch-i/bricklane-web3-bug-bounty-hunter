---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0-2-12
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-10-07T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-10-07-cyfrin-securitize-bridge-cctpv2-v2-0
title: Remove unused imports
vuln_class: []
---

# Remove unused imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-10-07-cyfrin-securitize-bridge-cctpv2-v2.0.md)_

---

**Description:** Remove unused imports:
* `USDCBridgeV2.sol`
```solidity
28:import {IBridge} from "./IBridge.sol";
```

**Securitize:** Fixed in commit [a45cb7e](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/a45cb7edcc9ec79c5e1cc30420c826e0566af827).

**Cyfrin:** Verified.
