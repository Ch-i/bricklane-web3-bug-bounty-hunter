---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-8
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`scripts/verify_deployment.ts` omissions'
vuln_class: []
---

# `scripts/verify_deployment.ts` omissions

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** The post-deploy verifier does not check several invariants: security-council address post-deployment, outflow-config activation timestamps, steward-budget initial state, whitelist-locked state after `clearDeployer`.

**Impact:** A misconfigured deployment may pass the automated check and require manual inspection to catch.

**Recommended Mitigation:** Extend `scripts/verify_deployment.ts` to cover each of the listed invariants.

**Armada:** Fixed in commit [efa2783](https://github.com/ship-armada/armada-poc/commit/efa2783d327640af00be2fafcc973c8e1502746f).

**Cyfrin:** Verified.
