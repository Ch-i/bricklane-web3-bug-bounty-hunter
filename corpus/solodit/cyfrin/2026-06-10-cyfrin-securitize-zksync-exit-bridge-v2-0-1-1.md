---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0-1-1
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-06-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2-0
title: Remove unused import `BaseDSContract` from `SecuritizeBridge.sol`
vuln_class: []
---

# Remove unused import `BaseDSContract` from `SecuritizeBridge.sol`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-10-cyfrin-securitize-zksync-exit-bridge-v2.0.md)_

---

**Description:** Remove unused import `BaseDSContract` from `SecuritizeBridge.sol`:
```diff
- import {BaseDSContract} from "@securitize/digital_securities/contracts/utils/BaseDSContract.sol";
```

**Securitize:** Fixed in commit [`884b16e`](https://github.com/securitize-io/bc-securitize-bridge-sc/commit/884b16e575a988d2c9bbcb806f9160a899b72657)

**Cyfrin:** Verified.

\clearpage
