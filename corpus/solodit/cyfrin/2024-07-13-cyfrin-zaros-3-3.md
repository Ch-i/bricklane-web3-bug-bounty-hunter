---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2024-07-13-cyfrin-zaros-3-3
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2024-07-13T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md
tags:
- firm:cyfrin
- report:2024-07-13-cyfrin-zaros
title: The `LogConfigureMarginCollateral` event doesn't emit `loanToValue`
vuln_class: []
---

# The `LogConfigureMarginCollateral` event doesn't emit `loanToValue`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2024-07-13-cyfrin.zaros.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2024-07-13-cyfrin.zaros.md)_

---

**Description:** The [LogConfigureMarginCollateral](https://github.com/zaros-labs/zaros-core-audit/blob/de09d030c780942b70f1bebcb2d245214144acd2/src/perpetuals/branches/GlobalConfigurationBranch.sol#L212) event omits `loanToValue` during a margin collateral configuration.

**Recommended Mitigation:** Recommend emitting `loanToValue` also.

**Zaros:** Fixed in commit [aef72cd](https://github.com/zaros-labs/zaros-core/commit/aef72cdc4319314c2a4b9497ba39a5621657f7b4).

**Cyfrin:** Verified.
