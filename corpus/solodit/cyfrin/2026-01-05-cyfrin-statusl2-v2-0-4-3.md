---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-4-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: Consider removing unused functions in libraries
vuln_class: []
---

# Consider removing unused functions in libraries

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** Functions `StakeMath::_estimateLockTime`, `MultiplierPointMath::_lockTimeAvailable`, `MultiplierPointMath::_timeToAccrueMP`, `MultiplierPointMath::_retrieveBonusMP`, `MultiplierPointMath::_retrieveAccruedMP` are internal in libraries and never used in protocol.

**Recommended Mitigation:** Consider removing them.

**StatusL2:** Acknowledged, the team stated that they will be implementing views functions for the UI.
