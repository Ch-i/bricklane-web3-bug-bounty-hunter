---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-24-cyfrin-yieldfi-v2-0-3-9
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-24T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-24-cyfrin-yieldfi-v2-0
title: Access to `LockBox::unlock` doesn't follow principle of least privilege
vuln_class: []
---

# Access to `LockBox::unlock` doesn't follow principle of least privilege

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-24-cyfrin-yieldfi-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-24-cyfrin-yieldfi-v2.0.md)_

---

**Description:** The function [`LockBox::unlock`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/core/l1/LockBox.sol#L97) has the modifier [`onlyBridgeOrLockBox`](https://github.com/YieldFiLabs/contracts/blob/40caad6c60625d750cc5c3a5a7df92b96a93a2fb/contracts/administrator/Access.sol#L37-L40) which allows callers with either the role `BRIDGE_ROLE` or `LOCKBOX_ROLE` to access the call.

The function is however only called from the bridge contracts. Consider removing the access from the `LOCKBOX_ROLE` to follow principle of least privileges.

**YieldFi:** Fixed in commit [`f0c751a`](https://github.com/YieldFiLabs/contracts/commit/f0c751a25d3cf8d46661f7508b72193c88e6fc91)

**Cyfrin:** Verified.

\clearpage
