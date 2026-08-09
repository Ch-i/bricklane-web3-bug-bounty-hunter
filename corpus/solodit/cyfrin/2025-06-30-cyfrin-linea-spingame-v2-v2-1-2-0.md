---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-30-cyfrin-linea-spingame-v2-v2-1-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-06-30T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-30-cyfrin-linea-spingame-v2-v2-1
title: Cache `signer` in `SpinGame::participate`
vuln_class: []
---

# Cache `signer` in `SpinGame::participate`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-30-cyfrin-linea-spingame-v2-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-30-cyfrin-linea-spingame-v2-v2.1.md)_

---

**Description:** In `SpinGame::participate`, the `signer` state variable is accessed multiple times:

```solidity
address recoveredSigner = ECDSA.recover(...);
if (recoveredSigner != signer || signer == address(0)) {
    revert SignerNotAllowed(recoveredSigner);
}
```

In contrast, `SpinGame::claimPrize` caches `signer` to a local variable (`cachedSigner`) before comparison. This avoids redundant storage reads, which are more expensive than local memory accesses.

Considerer caching `signer` in a local variable at the start of the relevant check in `SpinGame::participate` as well.

**Linea:** Fixed in commit [`0290123`](https://github.com/Consensys/linea-hub/pull/557/commits/02901233dbe9a184b80bffb67bf5d489bc015a10)

**Cyfrin:** Verified. `signer` is cached and the cached value is used in the comparisons.
