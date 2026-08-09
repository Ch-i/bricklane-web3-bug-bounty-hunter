---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-2
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`RevenueCounter` missing trailing storage gap despite UUPS upgradeability'
vuln_class: []
---

# `RevenueCounter` missing trailing storage gap despite UUPS upgradeability

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor` reserves `uint256[25] __gap` at its storage tail but `RevenueCounter` does not. The project deploys via raw `ERC1967Proxy` without the OpenZeppelin Upgrades plugin's layout-diff tooling. Any future upgrade that inserts a new state variable above `lastSyncedCumulative` silently shifts that slot.

**Impact:** Probability low, consequence severe: cumulative revenue is silently misread after a layout-breaking upgrade.

**Recommended Mitigation:** Consider adding storage gap at the bottom of `RevenueCounter`. Another way is to leave as it is, and use EIP7201 during upgrade.

**Armada:** Fixed in commit [c4f23d4](https://github.com/ship-armada/armada-poc/commit/c4f23d404346ce79b59fa30683ce5ea547eeecec).

**Cyfrin:** Verified.
