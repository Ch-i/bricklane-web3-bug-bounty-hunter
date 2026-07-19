---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-05-cyfrin-statusl2-v2-0-0-1
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-05T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-05-cyfrin-statusl2-v2-0
title: User can double claim airdrop
vuln_class: []
---

# User can double claim airdrop

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-05-cyfrin-statusl2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-05-cyfrin-statusl2-v2.0.md)_

---

**Description:** `KarmaAirdrop.sol` is pausable. That's because there is functionality to update `merkleRoot`: when it's updated, previously unclaimed tokens are added to the new `merkleRoot`. So following scenario is possible:
1) User have not claimed. `merkleRoot` will be updated to include some new people and previously unclaimed users
2) User frontruns upgrade by claiming his part
3) New `merkleRoot` now again contains his airdrop, so user can claim second time

To prevent this scenario, `KarmaAirdrop.sol` inherits `Pausable.sol`, however `KarmaAirdrop::claim` doesn't have `whenNotPaused` modifier

**Impact:** During `merkleRoot` upgrade, previously unclaimed users can double claim, stealing tokens.

**Recommended Mitigation:** Add modifier `whenNotPaused` to `KarmaAirdrop::claim`.

**StatusL2:** Fixed in [ebbf84b](https://github.com/status-im/status-network-monorepo/commit/ebbf84b63eb3b4559c93d130b883d78c9cb040f8).

**Cyfrin:** Verified.

\clearpage
