---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-09-08-cyfrin-greekfi-core-v2-0-2-4
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
title: '`IOption` documents the wrong pair-burn event'
vuln_class: []
---

# `IOption` documents the wrong pair-burn event

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-09-08-cyfrin-greekfi-core-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-09-08-cyfrin-greekfi-core-v2.0.md)_

---

**Description:** `IOption::transfer, burn` state that pair burns emit `Redeemed` from the Receipt and nothing from the Option. The implementation instead emits `PairBurned` from the Option, while `Receipt::burn` emits nothing.

**Recommended Mitigation:** Update the `IOption::transfer, burn` NatSpec to state that the Option emits `PairBurned` and the Receipt emits nothing. No implementation change is required.

**GreekFi:** Fixed in [PR46](https://github.com/greekfi/contracts/pull/46)

**Cyfrin:** Verified. The Option NatSpec now identifies PairBurned as the protocol event emitted by pair burns.
