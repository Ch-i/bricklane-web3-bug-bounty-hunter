---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-5-6
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Use `uint32` for timestamps for better storage packing
vuln_class: []
---

# Use `uint32` for timestamps for better storage packing

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** The maximum value of `uint32` is 4294967295 which is 2106/02/07 - likely far longer than required by this protocol! Using `uint32` instead of `uint256` for timestamps and making sure those variables are adjacent to each-other can result in significantly reducing the amount of storage slots required:

* `SessionManager::Game::startTime, endTime, originalStartTime`
* `SessionManager::minimumStartDelay, maxGameDuration, revealGracePeriod, livenessDuration`
* `DefaultSession::SessionResult::time`

**Majority Games:**
Fixed in commit [5902894](https://github.com/Engage-Protocol/engage-protocol/commit/5902894a3c21e684298b639307ec950bc34be74b).

**Cyfrin:** Verified.
