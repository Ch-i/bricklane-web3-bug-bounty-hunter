---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-09-04-cyfrin-symbiotic-v2-0-2-0
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2025-09-04T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md
tags:
- firm:cyfrin
- report:2025-09-04-cyfrin-symbiotic-v2-0
title: '`OpNetVaultAutoDeployLogic::getVetoSlasherParams` is never used'
vuln_class: []
---

# `OpNetVaultAutoDeployLogic::getVetoSlasherParams` is never used

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-09-04-cyfrin-symbiotic-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-09-04-cyfrin-symbiotic-v2.0.md)_

---

**Description:** `OpNetVaultAutoDeployLogic::getVetoSlasherParams` is dead code that is never used. It is also worth noting that `OpNetVaultAutoDeploy` is designed only for `InstantSlasher` and has no mechanism to utilize `VetoSlasher` functionality.

**Recommended Mitigation:** Consider removing the function `getVetoSlasherParams` from the `OpNetVaultAutoDeployLogic` library.

**Symbiotic:** Acknowledged. Unchanged to simplify external customizations

**Cyfrin:** Acknowledged.
