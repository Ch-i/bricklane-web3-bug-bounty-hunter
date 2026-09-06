---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-02-20-cyfrin-aarc-btcy-v2-0-2-10
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-02-20T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md
tags:
- firm:cyfrin
- report:2026-02-20-cyfrin-aarc-btcy-v2-0
title: Inconsistent naming of `IBTCYHub::_processRedemption` return value
vuln_class: []
---

# Inconsistent naming of `IBTCYHub::_processRedemption` return value

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-02-20-cyfrin-aarc-btcy-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-02-20-cyfrin-aarc-btcy-v2.0.md)_

---

**Description:** `IBTCYHub::_processRedemption` returns `(fee, ibtcyToBurn)`, but `IBTCYHub::_processRedemptionBatch` assigns the second value to `processedAmount` and then sums it into `totalIBTCYTokensToBurn`. Since “processed amount” typically implies the total (burn + fees), this naming is easy to misinterpret.

Consider renaming the local variable in `_processRedemptionBatch` to `ibtcyToBurn`.

**Aarc:** Fixed in commit [99b97a5](https://github.com/aarc-xyz/btcy-contracts-main/commit/99b97a55a6a3342042dd78b21ac47abf38e24f78).

**Cyfrin:** Verified.
