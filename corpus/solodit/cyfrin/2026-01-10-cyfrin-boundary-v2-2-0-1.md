---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-1
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: '`FULL` restriction can be bypassed'
vuln_class: []
---

# `FULL` restriction can be bypassed

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** `sUSBD` enforces `RestrictedStatus.FULL` by blocking *transfers* in `_update()` only when both `from != address(0)` and `to != address(0)`. However, restriction is applied per-address and is not “sticky” to the shares themselves. If an account anticipates being set to `FULL`, it can front-run the `setRestrictedStatus(account, FULL)` transaction by transferring its sUSBD shares to a fresh address that is not restricted. Once the restriction update lands, the original address is frozen, but the shares have already been moved and remain fully usable from the new address.

**Impact:** `FULL` restriction can be bypassed.

**Proof of Concept:**
1. `victim` holds `N` sUSBD shares.
2. `RESTRICTION_MANAGER_ROLE` submits `setRestrictedStatus(victim, FULL)` to the mempool.
3. `victim` observes the pending tx and submits `transfer(newAddr, N)` with higher priority (front-runs).
4. `transfer` succeeds because `victim` is not yet `FULL` (and `newAddr` is unrestricted).
5. `setRestrictedStatus(victim, FULL)` executes afterward; `victim` is frozen but now holds `0` shares. The shares are controlled by `newAddr` and can be withdrawn/transferred normally.

**Recommended Mitigation:** Full mitigation of this issue requires significant reworking. For example, a short lock could be introduced during transfer shares. Another possible solution is to ensure that any transactions blocking users is done through flashbots / private mempool and have this properly documented.

**Boundary:**
Acknowledged. We recognize this as an operational challenge. Administrative transactions will be submitted through private mempools to prevent front-running.
