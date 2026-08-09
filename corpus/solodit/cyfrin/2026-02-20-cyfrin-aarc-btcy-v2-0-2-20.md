---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-20
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: User can front-run DoS `DepositWithdraw::withdrawTransfer` by cancelling redemption
  request
vuln_class: []
---

# User can front-run DoS `DepositWithdraw::withdrawTransfer` by cancelling redemption request

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** A user can front-run calls to `DepositWithdraw::withdrawTransfer` by cancelling their redemption request, which makes the entire batch revert.

**Recommended Mitigation:** Can likely just be acknowledged as low risk, not worth adding more complexity to the code. If it ever becomes an issue use a private mempool service like flashbots.

**Aarc:** Acknowledged.

\clearpage
