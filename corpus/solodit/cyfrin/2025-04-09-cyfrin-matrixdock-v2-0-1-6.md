---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Use named imports
vuln_class: []
---

# Use named imports

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** The contracts mostly use named imports but strangely some import statements don't; use named imports everywhere:

`MTokenMessager`:
```solidity
import "./interfaces/ICCIPClient.sol";
```

`MTokenMessagerLZ`:
```solidity
import "./MTokenMessagerBase.sol";
import "./interfaces/ICCIPClient.sol";
```

`MTokenMessagerV2`:
```solidity
import "./interfaces/ICCIPClient.sol";
import "./MTokenMessagerLZ.sol";
```

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b) for `MTokenMessagerLZ` and `MTokenMessagerV2`.

**Cyfrin:** Verified.
