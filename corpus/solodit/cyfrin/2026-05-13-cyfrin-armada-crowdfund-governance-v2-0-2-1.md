---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Pre-wind-down shield pause bleeds into post-wind-down; SC extends emergency
  window
vuln_class: []
---

# Pre-wind-down shield pause bleeds into post-wind-down; SC extends emergency window

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ShieldPauseController::pauseShields` (`:107-120`) writes `windDownPauseUsed = true` only when called while `windDownActive == true`. The SC can chain pauses across the trigger:

1. T0: SC calls `pauseShields` while `windDownActive == false` — state becomes `_paused=true`, `pauseExpiry=T0+24h`, `windDownPauseUsed=false`.
2. T1 (between T0 and T0+24h): permissionless `triggerWindDown` fires; `setWindDownActive` at `:147-152` flips `windDownActive = true` but does not touch `_paused`, `pauseExpiry`, or `windDownPauseUsed`. `emergencyPaused() == true` continues until `pauseExpiry`.
3. T0+25h: SC calls `pauseShields` again; `!_isPaused` passes, `windDownActive && !windDownPauseUsed` passes, and a fresh 24h pause consumes the single post-wind-down budget.

Total continuous unshield-blocking: ~48h against the documented 24h.

**Spec-Intent Gap:**

`specs/GOVERNANCE.md` §Wind-Down §Post-wind-down:

> The Security Council retains a **single non-renewable 24h pause authority only** ... the pause **cannot be renewed post-wind-down**. Enforcement: as part of `triggerWindDown()`, the wind-down contract sets a `windDownActive` flag on the pause contract. The pause mechanism checks: if `windDownActive && pauseAlreadyInvoked`, revert.

Code faithfully implements the spec's literal enforcement rule ("if `windDownActive && pauseAlreadyInvoked`, revert"), but the rule misses the pre-trigger case — a pause issued while `windDownActive == false` leaves `pauseAlreadyInvoked` (`windDownPauseUsed`) at `false`. Both the spec's enforcement sentence and the code need the same fix; relying on the spec sentence alone will not close the bleed path.

**Recommended Mitigation:** Explicitly define correct behaviour in spec and update code if necessary.

**Armada:** Fixed in commit [a33407c](https://github.com/ship-armada/armada-poc/commit/a33407cb6018680935e7bd7750200117c9783dbf).

**Cyfrin:** Verified.
