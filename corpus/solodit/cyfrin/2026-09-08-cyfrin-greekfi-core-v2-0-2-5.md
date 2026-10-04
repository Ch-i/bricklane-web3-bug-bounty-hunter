---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-5
ingested_at: '2026-10-04T10:45:09Z'
protocol_category: []
published_at: '2026-09-08T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md
tags:
- firm:cyfrin
- report:2026-09-08-cyfrin-greekfi-core-v2-0
title: '`Receipt::sweep` can clear accrued fee accounting without reporting the cleared
  amount'
vuln_class: []
---

# `Receipt::sweep` can clear accrued fee accounting without reporting the cleared amount

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `Receipt::sweep` resets `feeAccrued[token]` to its 1-wei floor before transferring the token balance. The `Swept` event reports only the total transfer, so off-chain accounting cannot determine how much accrued fee was cleared. On-chain accounting remains correct.

**Recommended Mitigation:** Emit the cleared fee amount, either in `Swept` or in a dedicated event.

**GreekFi:** Fixed in [PR43](https://github.com/greekfi/contracts/pull/43)

**Cyfrin:** Verified. Receipt now emits FeeCleared with the accrued-fee amount removed from accounting during a sweep.
