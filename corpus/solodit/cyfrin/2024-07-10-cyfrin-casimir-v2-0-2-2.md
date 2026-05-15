---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-10-cyfrin-casimir-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-07-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md
tags:
- firm:cyfrin
- report:2024-07-10-cyfrin-casimir-v2-0
title: Missing implementation for  EigenPod `withdrawNonBeaconChainETHBalanceWei`
  in CasimirManager
vuln_class: []
---

# Missing implementation for  EigenPod `withdrawNonBeaconChainETHBalanceWei` in CasimirManager

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-10-cyfrin-casimir-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-10-cyfrin-casimir-v2.0.md)_

---

**Description:** EigenLayer has a function `EigenPod::withdrawNonBeaconChainETHBalanceWei` that is intended to be called by the pod owner to sweep any ETH donated to EigenPod. Currently, there seems to be no way to withdraw this balance from EigenPod.

**Impact:** Donations to EigenPod are essentially stuck while the pod is active.

**Recommended Mitigation:** Consider adding a function to `CasimirManager` that sweeps the `nonBeaconChainETH` balance and sends it to `distributeStakes`, similar to `CasimirManager::claimTips`.

**Casimir:**
Fixed in [790817a](https://github.com/casimirlabs/casimir-contracts/commit/790817a9ba615dbcd7c85d449fe7aa19c02371b7)

**Cyfrin:** Verified.
