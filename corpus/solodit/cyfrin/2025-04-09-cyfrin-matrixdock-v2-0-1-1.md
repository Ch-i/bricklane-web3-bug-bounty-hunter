---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Use named mappings
vuln_class: []
---

# Use named mappings

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** Use named mappings to explicity indicate purpose of index => value:
```solidity
MTokenMessager.sol
16:    mapping(uint64 => mapping(address => bool)) public allowedPeer;
//     mapping(uint64 chainSelector => mapping(address messager => bool allowed)) public allowedPeer;

MTokenMessagerV2.sol
28:    mapping(uint64 => mapping(address => bool)) public allowedPeer;
//     mapping(uint64 chainSelector => mapping(address messager => bool allowed)) public allowedPeer;
```

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-f1dbc2c2c340ac285844595cba6f20040bb8b33c2ae726867955370039433c6aR11-R28) for `MTokenMessagerV2`.

**Cyfrin:** Resolved.
