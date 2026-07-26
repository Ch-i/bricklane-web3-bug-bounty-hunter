---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-2-5
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
title: '`ArmadaGovernor::securityCouncil` is inert at launch; no deploy-time bootstrap'
vuln_class: []
---

# `ArmadaGovernor::securityCouncil` is inert at launch; no deploy-time bootstrap

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** `ArmadaGovernor::securityCouncil` defaults to `address(0)`. `setSecurityCouncil` is timelock-only, so activating the SC requires a passed and executed governance proposal. Until that happens, veto actions and SC-gated `pauseShields` revert with `Gov_SCEjected`. Governance itself requires quorum (floor = 100k ARM); before sufficient delegation occurs, the quorum may be unmeetable. `scripts/deploy_governance.ts` never initializes the SC.

**Impact:** Launch window during which no SC exists - any early proposal cannot be vetoed.

**Recommended Mitigation:** Consider setting initial security council by deployer.

**Armada:** Fixed in commit [79e518c](https://github.com/ship-armada/armada-poc/commit/79e518ce3e52eb620afa7525f95a943d4f16601c).

**Cyfrin:** Verified; one concern is that this allows the deployer to change the security council at any time, however this is mitigated by `ArmadaGovernor::clearDeployer` being called after a successful deployment (see `scripts/deploy_crowdfund.ts` and `verify_deployment.ts`).
