---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-06-cyfrin-wlfi-unlock-v2-0-2-5
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-06T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-06-cyfrin-wlfi-unlock-v2-0
title: WLFI pause does not block retail elections, only team elections and Vester-gated
  flows
vuln_class: []
---

# WLFI pause does not block retail elections, only team elections and Vester-gated flows

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-06-cyfrin-wlfi-unlock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-06-cyfrin-wlfi-unlock-v2.0.md)_

---

**Description:** The V3 election flow interacts with two independent pause states — WorldLibertyFinancialV3 (pausable via ownerPause/guardianPause, inherited from V2) and WorldLibertyFinancialVester (pausable via ownerPause/guardianPause). Neither `electVestingUpdate` nor `ownerElectVestingUpdatesFor` has whenNotPaused on V3 itself; pause semantics are entirely downstream.

Downstream reach:

- `Vester.wlfiSetCategory` — whenNotPaused (line 158). Invoked for BOTH retail and team elections.
- `Vester.wlfiBurnAllocation` — whenNotPaused (line 103). Invoked only for team (cat 47) elections.
- `WLFI.burn` (via Vester's wlfiBurnAllocation) — routed through V2's _update which is ERC20PausableUpgradeable.whenNotPaused. Invoked only for team elections.

An operator who pauses WLFI during an incident expecting to halt all new elections will find retail elections still land, mutating Registry + Vester category state. Only pausing the Vester achieves a uniform halt.

**Impact:** A retail user with a valid signature can still flip their category to 45 while WLFI is paused.

**Recommended Mitigation:** Consider adding `whenNotPaused` check to the `WorldLibertyFinancialV3::electVestingUpdate` and `WorldLibertyFinancialV3::ownerElectVestingUpdatesFor` entry points.

**WLFI:** Fixed in commit [1430e24](https://github.com/worldliberty/usd1-protocol/commit/1430e245349795921bebe275f6bd1d835d9f8fa3).

**Cyfrin:** Verified.
