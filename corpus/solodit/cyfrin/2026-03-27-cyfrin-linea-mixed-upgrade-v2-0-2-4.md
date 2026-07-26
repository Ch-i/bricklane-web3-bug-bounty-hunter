---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-2-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: Missing `onlyInitializing` modifier on initialization functions for abstract
  contracts
vuln_class: []
---

# Missing `onlyInitializing` modifier on initialization functions for abstract contracts

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** The `onlyInitializing` modifier is the established standard for protecting internal initialization functions in abstract contracts against unintended calls post-initialization. These new initialization functions introduced here do not include this modifier, which deviates from common security patterns:
* `L2MessageServiceBase::__L2MessageService_init`
* `LineaRollupBase::__LineaRollup_init`
* `TokenBridgeBase::__TokenBridge_init`

**Recommended Mitigation:** Consider adding the `onlyInitializing` modifier to those functions.

**Linea:** Fixed in commits [802cf72](https://github.com/Consensys/linea-monorepo/pull/2007/commits/802cf7239754526861e1e8777380619e8bc39cf2), [2d63895](https://github.com/Consensys/linea-monorepo/commit/2d638959adec0c13f66d72bb6c44b16f7df4bea1).

**Cyfrin:** Verified.
