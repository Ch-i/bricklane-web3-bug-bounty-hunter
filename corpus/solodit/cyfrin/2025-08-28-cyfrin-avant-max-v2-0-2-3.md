---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-2-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Modifier `mintRequestExist` can be safely removed from `RequestsManager::cancelMint,
  cancelBurn` saving 1 identical storage read
vuln_class: []
---

# Modifier `mintRequestExist` can be safely removed from `RequestsManager::cancelMint, cancelBurn` saving 1 identical storage read

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** `RequestsManager::cancelMint` validates that `request.provider == msg.sender`:
```solidity
L152:    _assertAddress(request.provider, msg.sender);
```

Hence the modifier `mintRequestExist(_id)` can be safely removed to save 1 identical storage read of `mintRequests[_id].provider`.

The same applies to `RequestsManager::cancelBurn`.

**Avant:**
Fixed in commit [f74d1fc](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/f74d1fc334cf34f8751285e55cf44e41238859e1).

**Cyfrin:** Verified.
