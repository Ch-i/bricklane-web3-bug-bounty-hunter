---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-04-09-cyfrin-matrixdock-v2-0-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-04-09T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md
tags:
- firm:cyfrin
- report:2025-04-09-cyfrin-matrixdock-v2-0
title: Don't allow pausing for LayerZero receive, only send
vuln_class: []
---

# Don't allow pausing for LayerZero receive, only send

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2025-04-09-cyfrin-matrixdock-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-04-09-cyfrin-matrixdock-v2.0.md)_

---

**Description:** `MTokenMessagerLZ` has the `onlyLZNotPaused` modifier on both the receiving function `_lzReceive` and the two sending functions `lzSendTokenToChain` / `lzSendMintBudgetToChain`.

Consider removing the `onlyLZNotPaused` modifier from `_lzReceive`  as the sender has already burned their tokens when sending, so don't want receiving to revert in this case.

**Matrixdock:** Fixed in commit [f3fbe97](https://github.com/Matrixdock-RWA/RWA-Contracts/commit/f3fbe97bd20ad514b76aa422a7dfc1f8a66cd66b#diff-591d4d35e5121caa982af913bb68ff10a5555b9462a19650bfd5b844ecedee43L46).

**Cyfrin:** Verified.
