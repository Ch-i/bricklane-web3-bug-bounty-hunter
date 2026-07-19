---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-2-3
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: Not emitting event to log the version's change when reinitializing the `LineaRollup`
  contract
vuln_class: []
---

# Not emitting event to log the version's change when reinitializing the `LineaRollup` contract

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** When `LineaRollup` gets upgraded, [`LineaRollup::reinitializeV8`](https://github.com/Consensys/linea-monorepo/blob/main/contracts/src/rollup/LineaRollup.sol#L52-L67) is called to reinitialize permissions, roles, set the `shnarfProvider`, and bump up the `initialized` version, but `LineaRollupVersionChanged` event is not emitted to log the version's change.

**Recommended Mitigation:** Emit the event `LineaRollupVersionChanged` with the respective `previousVersion` and `newVersion` for the `LineaRollup`.

**Linea:** Fixed in [PR2020](https://github.com/Consensys/linea-monorepo/pull/2020).

**Cyfrin:** Verified.
