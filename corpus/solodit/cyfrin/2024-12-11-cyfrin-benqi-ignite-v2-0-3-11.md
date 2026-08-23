---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-12-11-cyfrin-benqi-ignite-v2-0-3-11
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2024-12-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md
tags:
- firm:cyfrin
- report:2024-12-11-cyfrin-benqi-ignite-v2-0
title: Magic numbers should be replaced by constant variables
vuln_class: []
---

# Magic numbers should be replaced by constant variables

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-12-11-cyfrin-benqi-ignite-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-12-11-cyfrin-benqi-ignite-v2.0.md)_

---

**Description:** The magic numbers `10_000`, `2000e18`, `201`/`201e18` are used throughout the `Ignite` contract but should be made constant variables instead.

**Recommended Mitigation:** Use constants in place of the magic numbers outlined above.

**BENQI:** Acknowledged, won’t change.

**Cyfrin:** Acknowledged.
