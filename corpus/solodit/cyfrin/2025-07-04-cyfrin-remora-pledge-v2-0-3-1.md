---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-07-04-cyfrin-remora-pledge-v2-0-3-1
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2025-07-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md
tags:
- firm:cyfrin
- report:2025-07-04-cyfrin-remora-pledge-v2-0
title: Rename `isAllowed` to `wasAllowed` in `Allowlist::allowUser`, `disallowUser`
vuln_class: []
---

# Rename `isAllowed` to `wasAllowed` in `Allowlist::allowUser`, `disallowUser`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-07-04-cyfrin-remora-pledge-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-07-04-cyfrin-remora-pledge-v2.0.md)_

---

**Description:** `Allowlist::allowUser`, `disallowUser` return the existing `allowed` status into a named return variable called `isAllowed`, before potentially modifying the `allowed` status.

Since these functions can modify the `allowed` status, the named return variable should be renamed to `wasAllowed` to explicitly indicate the returned status may not be current.

**Remora:** Fixed in commit [06d17a6](https://github.com/remora-projects/remora-smart-contracts/commit/06d17a68320472e44a46c59ff3623af3741f691a).

**Cyfrin:** Verified.
