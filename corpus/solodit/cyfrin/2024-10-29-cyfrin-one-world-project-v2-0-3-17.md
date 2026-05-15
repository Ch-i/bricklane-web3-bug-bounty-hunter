---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-10-29-cyfrin-one-world-project-v2-0-3-17
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2024-10-29T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md
tags:
- firm:cyfrin
- report:2024-10-29-cyfrin-one-world-project-v2-0
title: DAOs can be created with non-zero `TierConfig::minted`
vuln_class: []
---

# DAOs can be created with non-zero `TierConfig::minted`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-10-29-cyfrin-one-world-project-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-10-29-cyfrin-one-world-project-v2.0.md)_

---

**Description:** When creating a new DAO membership, there is no validation on the `minted` member of the parallel `TierConfig` structs, meaning that DAOs can be created with non-zero minted tokens even when the supply for a given tier index is actually zero.

**Recommended Mitigation:** Consider enforcing that tier configuration minted states should begin empty.

**One World Project:** Added check in [`09b6f0f`](https://github.com/OneWpOrg/smart-contracts-blockchain-1wp/commit/09b6f0f978d2a8d2952a6938bf5756bec8a0170d).

**Cyfrin:** Verified. Check added when pushing the tiers to `dao.tiers`.
