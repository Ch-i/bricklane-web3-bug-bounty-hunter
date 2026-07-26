---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-08-28-cyfrin-avant-max-v2-0-2-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-08-28T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md
tags:
- firm:cyfrin
- report:2025-08-28-cyfrin-avant-max-v2-0
title: Use `msg.sender` when calling `safeTransfer` in `RequestsManager::cancelMint,
  cancelBurn`
vuln_class: []
---

# Use `msg.sender` when calling `safeTransfer` in `RequestsManager::cancelMint, cancelBurn`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-08-28-cyfrin-avant-max-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-08-28-cyfrin-avant-max-v2.0.md)_

---

**Description:** `RequestsManager::cancelMint` first enforces that `request.provider == msg.sender`:
```solidity
    _assertAddress(request.provider, msg.sender);
```

Hence it can directly use `msg.sender` instead of `request.provider` to save 1 storage read when calling `safeTransfer`:
```diff
-   depositedToken.safeTransfer(request.provider, request.amount);
+   depositedToken.safeTransfer(msg.sender, request.amount);
```

The same applies to `RequestsManager::cancelBurn`.

**Avant:**
Fixed in commit [7a3587c](https://github.com/Avant-Protocol/Avant-Contracts-Max/commit/7a3587ca6d673d143565703d094b6f9526fd8020).

**Cyfrin:** Verified.
