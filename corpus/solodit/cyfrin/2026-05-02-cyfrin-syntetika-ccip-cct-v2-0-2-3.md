---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-3
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`Minter::totalDeposits` accounting drifts from both reserves and synthetic
  supply across every privileged path'
vuln_class: []
---

# `Minter::totalDeposits` accounting drifts from both reserves and synthetic supply across every privileged path

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `totalDeposits` is documented as "total amount of base asset currently held in the Minter." Mutation table:

| Path | totalDeposits | baseAsset change | hilSynth change |
|---|---|---|---|
| `mint` | +amount | +amount | +amount |
| `redeem` | -amount | -amount | -amount |
| `ownerMint` | +amount | 0 | +amount |
| `distributeYield` | +amount | 0 | +amount |
| `transferToCustody` | 0 | -amount | 0 |
| `realizeLosses` | 0 | 0 | -amount |

Consequences: `totalDeposits != baseAsset_held + custody` (broken by `ownerMint`, `distributeYield`, `realizeLosses`) and `totalDeposits != hilSynth.totalSupply()` (broken by `realizeLosses`). Additionally, `transferToCustody` has no caps - operator can drain all Minter reserves in one call, while `totalDeposits` remains stale. Users redeeming afterwards get `ERC20InsufficientBalance` on the baseAsset transfer, DoSing redemption despite the accounting showing full backing.

Source: `issuance/src/minter/Minter.sol:244, 259, 391-398, 431-440`.

**Impact:** Off-chain dashboards, PoR attestations, and any future contract logic that reads `totalDeposits` (e.g., CCT hooks, cap enforcement) receive misleading values. Redemption is DoSable by operator action with no on-chain safeguard. Related to the unbacked-mint issue - both stem from unreconciled accounting.

**Recommended Mitigation:** Decide the semantic - live reserves vs. outstanding liability - and enforce consistently. Preferred: remove `totalDeposits` entirely and derive from `baseAsset.balanceOf(address(this))`. Alternatively, add a minimum reserve floor enforced on `transferToCustody`: `require(baseAsset.balanceOf(this) - amount >= totalDeposits * minReserveBps / BPS)`.

**Syntetika:** Fixed in commit [`bae5a23`](https://github.com/SyntetikaLabs/monorepo/commit/bae5a238f0bb181411a5990e1504003efd0bf71b)

**Cyfrin:** Verified. `totalDeposits` removed.
