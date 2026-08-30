---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Consider enforcing minimum deposit amount
vuln_class: []
---

# Consider enforcing minimum deposit amount

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `BTCY` enforces a minimum withdrawal amount but consider also enforcing a minimum deposit amount.

It is good defensive practice to prevent very small deposits and withdrawals (especially 1 wei) since these transaction patterns are not used by legitimate users but are used by blackhats to manipulate vaults. Affected contracts:

* `BTCY.sol`

**Aarc:** Fixed in commit [30c4800](https://github.com/aarc-xyz/btcy-contracts-main/commit/30c4800db02499a12e27ad689a2e7ace6f230506).

**Cyfrin:** Verified.
