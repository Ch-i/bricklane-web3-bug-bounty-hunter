---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Use named mapping parameters to make explicit the purpose of keys and values
vuln_class: []
---

# Use named mapping parameters to make explicit the purpose of keys and values

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** Named mapping parameters are already being used in almost all of the codebase, the one exception is:
```solidity
SimpleToken.sol
13:  mapping(bytes32 => bool) private mintIds;
14:  mapping(bytes32 => bool) private burnIds;
```

**Avant:**
Fixed in commit [1cc43e3](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/1cc43e3c59baa16b5b529ad06fee637bd6131ec1).

**Cyfrin:** Verified.
