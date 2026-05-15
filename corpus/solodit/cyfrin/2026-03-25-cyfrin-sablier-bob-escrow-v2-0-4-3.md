---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-03-25-cyfrin-sablier-bob-escrow-v2-0-4-3
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-03-25T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md
tags:
- firm:cyfrin
- report:2026-03-25-cyfrin-sablier-bob-escrow-v2-0
title: Remove or resolve TODO
vuln_class: []
---

# Remove or resolve TODO

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-03-25-cyfrin-sablier-bob-escrow-v2.0.md)_

---

**Description:** Remove or resolve TODO:
```solidity
SablierBob.sol
330:                // TODO: transfer entire fee to comptroller admin instead of transferring when user redeems.
```

**Sablier:** Fixed in commit [7928553](https://github.com/sablier-labs/lockup/commit/79285536d2dde653c0a7629785787ffb79f548f6#diff-f327a4238131660e66994c40e1d9f1ddd672c4403ed6f4ca2f1e04f7c82a86c3L330).

**Cyfrin:** Verified.
