---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-06-11-cyfrin-strata-v2-1-3-8
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2025-06-11T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md
tags:
- firm:cyfrin
- report:2025-06-11-cyfrin-strata-v2-1
title: Inconsistency in `currentPhase` between `pUSDeVault` and `yUSDeVault`
vuln_class: []
---

# Inconsistency in `currentPhase` between `pUSDeVault` and `yUSDeVault`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-06-11-cyfrin-strata-v2.1.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-06-11-cyfrin-strata-v2.1.md)_

---

**Description:** Both `pUSDeVault` and `yUSDeVault` inherit the `PreDepositVault` which in turn inherits the `PreDepositPhaser`; however, there is an inconsistency between the state of `pUSDe::currentPhase`, which is updated when the phase changes, and `yUSDe::currentPhase`, which is never updated and is thus always the default `PointsPhase` variant. This is assumedly not an issue given that this state is never needed for the yUSDe vault, though a view function is exposed by virtue of the state variable being public which could cause confusion.

**Recommended Mitigation:** The simplest solution would be modifying this state to be internal by default and only expose the corresponding view function within `pUSDeVault`.

**Strata:** Fixed in commit [aac3b61](https://github.com/Strata-Money/contracts/commit/aac3b617084fb5a06b29728a9f52e5884b062b6a).

**Cyfrin:** Verified. The `yUSDeVault` now returns the `pUSDeVault` phase state.

\clearpage
