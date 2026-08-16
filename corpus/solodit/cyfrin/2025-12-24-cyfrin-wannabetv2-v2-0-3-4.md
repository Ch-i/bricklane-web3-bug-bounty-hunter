---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-3-4
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Gas
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Remove redundant timestamp check in `Bet::resolve`
vuln_class: []
---

# Remove redundant timestamp check in `Bet::resolve`

_Section severity (from Solodit section header): Gas_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** `Bet::resolve` has this revert check:
```solidity
// Make sure the bet is active
if (_status(b) != IBet.Status.ACTIVE || block.timestamp > b.resolveBy) {
    revert InvalidStatus();
}
```

But the call to `_status(b)` already checks `block.timestamp > b.resolveBy` and returns `EXPIRED` status which triggers the revert, so having the same timestamp check here again is redundant.

**WannaBet:** Fixed in commit [45afa44](https://github.com/gskril/wannabet-v2/commit/45afa44a0adf423a2c2775c22d9f99e0ce555bbc).

**Cyfrin:** Verified.

\clearpage
