---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-13-cyfrin-armada-crowdfund-governance-v2-0-3-9
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-13-cyfrin-armada-crowdfund-governance-v2-0
title: '`CROWDFUND_OPEN_DELAY` default 60 seconds is operationally fragile'
vuln_class: []
---

# `CROWDFUND_OPEN_DELAY` default 60 seconds is operationally fragile

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-13-cyfrin-armada-crowdfund-governance-v2.0.md)_

---

**Description:** Sixty-second grace between deploy and window open is too short for a production checklist to catch misconfiguration before commits start flowing.

**Impact:** Operational fragility: a rushed deploy may allow commits before the final verification checklist completes.

**Recommended Mitigation:** Raise the local-env default to e.g. 5 minutes and document the production value explicitly.

**Armada:** Fixed in commit [f40ad63](https://github.com/ship-armada/armada-poc/commit/f40ad63c71470e4301119f85d25b321d5305eda3).

**Cyfrin:** Verified.
