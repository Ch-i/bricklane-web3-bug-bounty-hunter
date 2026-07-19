---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-11
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Minter::distributeYield` missing `whenNotPaused`'
vuln_class: []
---

# `Minter::distributeYield` missing `whenNotPaused`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Every externally-callable state-mutating function in `Minter` is gated by `whenNotPaused` except three that create synthetic supply:

| Function | `whenNotPaused` |
|---|---|
| `mint` (L405) | ✓ |
| `redeem` (L419) | ✓ |
| `transferToCustody` (L392) | ✓ |
| `realizeLosses` (L432) | ✓ |
| `distributeYield` (L250) | **MISSING** |
| `ownerMint` (L232) | Admin |
| `requestOwnerMint` (L219) | Admin |

`Distributor::distributeYield` is permissionless (rate-limited by `timeLock`). When `Minter` is paused, a bot or attacker can still call `Distributor::distributeYield → Minter::distributeYield`, minting new synthetic supply and inflating `totalDeposits`. If the pause was triggered in response to an oracle/feed compromise, the attacker-controlled feed value continues to propagate through the vault despite the emergency halt.

**Impact:** The pause-induced freeze of user-visible flows (`mint`, `redeem`) creates a false sense of containment. The two supply-creation paths that actually matter for an oracle or admin-key compromise continue operating. Emergency responders believe the system is frozen; it is not.

**Recommended Mitigation:** Add `whenNotPaused` to `Minter::distributeYield` (line 250). If yield-during-pause is intentional, document the asymmetry explicitly.

**Syntetika:** Fixed in commit [`b58ab42`](https://github.com/SyntetikaLabs/monorepo/commit/b58ab42f0869e718a466c17af13b99ff93bc13af)

**Cyfrin:** Verified.
