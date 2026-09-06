---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Unused event `OwnershipTransferRequested` in `MTokenMessagerLZ`
vuln_class: []
---

# Unused event `OwnershipTransferRequested` in `MTokenMessagerLZ`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** The `MTokenMessagerLZ` contract declares an `OwnershipTransferRequested` event but never emits it anywhere in the contract. This suggests there might have been plans to implement a timelock mechanism for ownership transfer, but it was not completed. The event is defined but remains unused, which could indicate incomplete functionality.

```solidity
18:     event OwnershipTransferRequested(address indexed from, address indexed to);
```

**Matrixdock:** Removed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-591d4d35e5121caa982af913bb68ff10a5555b9462a19650bfd5b844ecedee43L18-R30).

**Cyfrin:** Verified.
