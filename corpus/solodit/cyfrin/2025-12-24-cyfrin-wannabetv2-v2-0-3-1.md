---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-3-1
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Don't copy entire structs from `storage` to `memory` when only a few slots
  are required
vuln_class: []
---

# Don't copy entire structs from `storage` to `memory` when only a few slots are required

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** Don't copy entire structs from `storage` to `memory` when only a few slots are required:
* `Bet::cancel` only needs to read 5 slots `status,maker,makerStake,takerStake,asset` from storage, so save 2 storage reads

Consider caching the required storage slots as they are needed, so that if a revert check triggers the code didn't waste a ton of gas reading a bunch of storage slots that never get used.

**WannaBet:** Acknowledged.
