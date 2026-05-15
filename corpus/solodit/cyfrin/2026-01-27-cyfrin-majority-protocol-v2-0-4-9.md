---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-9
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Anyone should be able to conclude the game once winners have been determined
vuln_class: []
---

# Anyone should be able to conclude the game once winners have been determined

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Currently only the game creator can call `SessionManager::concludeGame`, even though at this point the winners have been determined.

**Impact:** If the game creator doesn't like who won, they can not conclude the game. The game could then be cancelled by users via `SessionManager::cancelGameIfCreatorMissing` to get their game fee refunded, but this allows a game creator to not pay out winners if they don't like who won.

**Recommended Mitigation:** Allow anyone to call `SessionManager::concludeGame`. Since during this time the game creator can also call `SessionManager::cancelGame`, perhaps allow a timeout period before anyone can call `SessionManager::concludeGame` using an offset from when the game entered the `End` state.

**Majority Games:**
Fixed in commit [dca8622](https://github.com/Engage-Protocol/engage-protocol/commit/dca86228c93ad73486766a8d06f0e63eb292ee26).

**Cyfrin:** Verified.
