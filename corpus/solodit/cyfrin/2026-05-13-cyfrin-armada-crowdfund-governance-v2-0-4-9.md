---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-4-9
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: Redundant `sc != address(0)` check in `ShieldPauseController::pauseShields`
vuln_class: []
---

# Redundant `sc != address(0)` check in `ShieldPauseController::pauseShields`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ShieldPauseController::pauseShields` at `contracts/governance/ShieldPauseController.sol:109`:

```solidity
require(msg.sender == sc && sc != address(0), "ShieldPauseController: not SC");
```

The `sc != address(0)` conjunct is always true when reached. `msg.sender` is never `address(0)` in any EVM call (the zero address has no key and cannot originate or forward a call), so `msg.sender == sc` already implies `sc != address(0)`. The extra EQ + AND is paid on every call without changing semantics.

Pre-launch state (when `governor.securityCouncil()` returns `address(0)`) is still correctly rejected by the first conjunct alone.

**Recommended Mitigation:**
```solidity
require(msg.sender == sc, "ShieldPauseController: not SC");
```

**Armada:** Fixed in commit [27638df](https://github.com/ship-armada/armada-poc/commit/27638df2cf4f5816aab933fce6bc82dedfaeb519).

**Cyfrin:** Verified.
