---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0-2-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-05-19T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md
tags:
- firm:cyfrin
- report:2025-05-19-cyfrin-stakedotlink-polygon-staking-v2-0
title: Missing check for `_feeBasisPoints > 0` in `PolygonStrategy::addFee`
vuln_class: []
---

# Missing check for `_feeBasisPoints > 0` in `PolygonStrategy::addFee`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-05-19-cyfrin-stakedotlink-polygon-staking-v2.0.md)_

---

**Description:** `PolygonStrategy::addFee` does not check if `_feeBasisPoints > 0` when adding a new fee element to the `fees` array. This is inconsistent with the `PolygonStrategy::updateFee` logic where `_feeBasisPoints = 0` triggers a removal of the fee element from the `fees` array.

**Recommended Mitigation:** Consider introducing a non-zero check to `_feeBasisPoints`.

**Stake.Link:** Acknowledged. Owner will ensure the correct value is set.

**Cyfrin:** Acknowledged.
