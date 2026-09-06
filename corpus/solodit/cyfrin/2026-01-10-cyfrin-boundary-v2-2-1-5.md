---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-1-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Cooldown Deactivation Instantly Unlocks Pending Cooldown Funds
vuln_class: []
---

# Cooldown Deactivation Instantly Unlocks Pending Cooldown Funds

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** The documentation does not clearly specify the behavior of funds that are already in the cooldown state when `cooldownDuration` is set to 0. In the current implementation, disabling cooldown allows users with pending cooldown balances in the silo to immediately withdraw their funds via `unstake()`, even if their original `cooldownEnd` timestamp has not been reached. This behavior may be non-obvious to integrators and users relying on the documentation, as it effectively cancels all ongoing cooldowns.

**Recommended Mitigation:** Explicitly document that setting cooldownDuration to 0 immediately unlocks all pending cooldown balances and allows instant withdrawal through unstake().

**Bounded:**
Resolved. Documentation clarified in [PR#170](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/170).

**Cyfrin:** Verified.
