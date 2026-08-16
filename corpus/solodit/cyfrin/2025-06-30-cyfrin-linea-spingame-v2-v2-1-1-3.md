---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-1-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Missing `_disableInitializers()` in constructor
vuln_class: []
---

# Missing `_disableInitializers()` in constructor

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** The `SpinGame` contract is upgradeable but does **not** call `_disableInitializers()` in its constructor. In upgradeable contract patterns, this call is a best practice to prevent the implementation (logic) contract from being initialized directly.

While this doesn’t affect the proxy’s behavior, it helps protect against accidental or malicious use of the implementation contract in isolation, especially in environments where both proxy and implementation contracts are visible, like block explorers.

Consider adding the following line to the constructor of the `SpinGame` contract:

```solidity
constructor(address _trustedForwarderAddress) ERC2771ContextUpgradeable(_trustedForwarderAddress) {
    _disableInitializers();
}
```

This ensures that the implementation contract cannot be initialized independently.

**Linea:** Fixed in commit [`9f9d9fd`](https://github.com/Consensys/linea-hub/pull/554/commits/9f9d9fd76d2672f572e31079b5811bf6f0f48eed)

**Cyfrin:** Verified. Constructor now calls `_disableInitializers`.
