---
affected_contracts: []
derives_from: []
id: solodit-zokyo-2022-08-25-boba-network-2-2
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2022-08-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md
tags:
- firm:zokyo
- report:2022-08-25-boba-network
title: No upgradeability pattern used despite indicators.
vuln_class: []
---

# No upgradeability pattern used despite indicators.

_Section severity (from Solodit section header): Informational_  
_Audit firm: Zokyo_  
_Source report: [2022-08-25-Boba Network.md](https://github.com/solodit/solodit_content/blob/main/reports/Zokyo/2022-08-25-Boba%20Network.md)_

---

**Description**

In contracts LzApp.sol and NonnlockingLzApp.sol you are leaving an empty reserved space, for possible future upgrades and also using the OwnableUpgradeable and Initializer contracts. However, there's no upgradability mechanism used, such as Openzeppelin's Upgradable Proxy.

**Recommendation**

If you're not intending to use this pattern, please refactor the contracts to reflect this, otherwise complete the implementation in this direction.

**Re-audit comment**

Acknowledged
