---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-06-18-cyfrin-linea-forced-txns-v2-0-1-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-06-18T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md
tags:
- firm:cyfrin
- report:2026-06-18-cyfrin-linea-forced-txns-v2-0
title: Use named mappings to explicitly denote the purpose of keys and values
vuln_class: []
---

# Use named mappings to explicitly denote the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-06-18-cyfrin-linea-forced-txns-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-06-18-cyfrin-linea-forced-txns-v2.0.md)_

---

**Description:** Use named mappings to explicitly denote the purpose of keys and values:
```solidity
AddressFilter.sol
15:  mapping(address => bool) internal filteredAddresses;
```

**Linea:** Fixed in commit [857c4b7](https://github.com/Consensys/linea-monorepo/pull/2297/changes/857c4b76c90244bf8c5c8bd66c0f74726ce0cd6b#diff-3eee1a32db90dd3af5aaa4b7c9cb7699d317f11a62132ac86294675e970c58f1L13-R13).

**Cyfrin:** Verified.
