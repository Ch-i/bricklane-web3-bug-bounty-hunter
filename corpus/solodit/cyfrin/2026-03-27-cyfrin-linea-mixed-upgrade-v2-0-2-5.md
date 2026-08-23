---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-27-cyfrin-linea-mixed-upgrade-v2-0-2-5
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-03-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-27-cyfrin-linea-mixed-upgrade-v2-0
title: Consider wiping slot 177 on Linea `L2MessageService` after upgrade
vuln_class: []
---

# Consider wiping slot 177 on Linea `L2MessageService` after upgrade

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-27-cyfrin-linea-mixed-upgrade-v2.0.md)_

---

**Description:** After the upgrade, `L2MessageService` repurposes slot 177 for `__gap_ReentrancyGuardUpgradeable` but previously this was used for `_status`.

Using `cast storage 0x508Ca82Df566dCD1B0DE8296e70a96332cD644ec 177 --rpc-url https://rpc.linea.build` shows that slot 177 has a value of 1, so ideally this would be wiped to clean it when changing the usage of this slot into a gap.

**Linea:** Fixed in commit [c462da0](https://github.com/Consensys/linea-monorepo/pull/2007/commits/c462da0574f4f60667c3c357a2be61443fc0ab7a).

**Cyfrin:** Verified.

\clearpage
