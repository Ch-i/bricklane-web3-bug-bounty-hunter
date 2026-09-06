---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`TreasurySteward::termStart` stale after `removeSteward`'
vuln_class: []
---

# `TreasurySteward::termStart` stale after `removeSteward`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `TreasurySteward::removeSteward` clears `currentSteward` but not `termStart`. `isStewardActive` short-circuits on the zero address so the stale timestamp is inert today, but a future refactor reading raw `termStart` without the guard would behave incorrectly.

**Impact:** Defense-in-depth gap; future refactors may rely on `termStart` in isolation and regress.

**Recommended Mitigation:** Also clear `termStart` inside `removeSteward` to avoid stale state.

**Armada:** Fixed in commit [fc208ed](https://github.com/ship-armada/armada-poc/commit/fc208ed3fbcce65aab32f0118275038a9cd0da6d).

**Cyfrin:** Verified.
