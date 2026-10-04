---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-1-0
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`FactoryDeployer::deploy` lets a front-runner invalidate a pre-mined vanity
  address'
vuln_class: []
---

# `FactoryDeployer::deploy` lets a front-runner invalidate a pre-mined vanity address

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `FactoryDeployer::deploy` is permissionless, and `owner` is not included in the CREATE2 commitment. A searcher can copy a pending deployment's `initCode` and salt, deploy first with a different owner, and occupy the expected vanity address.

The official deployment script detects the collision and reverts, so the hostile deployment is not accepted as official.

**Impact:** An attacker can delay a new-chain rollout and force the team to mine a new vanity address. They cannot take control of a Factory accepted by the official deployment process. The impact is limited to deployment griefing.

**Recommended Mitigation:** Submit deployments privately and withhold salts until confirmation. Future versions should bind the owner into the CREATE2 commitment or require signed deployment authorization.

**GreekFi:** Fixed in [PR32](https://github.com/greekfi/contracts/pull/32)

**Cyfrin:** Verified. FactoryDeployer now binds the intended owner into the CREATE2 salt, so a caller using a different owner derives a different address.
