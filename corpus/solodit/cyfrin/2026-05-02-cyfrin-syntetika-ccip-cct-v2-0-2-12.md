---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-12
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
title: '`BlacklistableUpgradeable::blacklist(address(0))` bricks all mint and burn
  paths across HilToken and StakingVault'
vuln_class: []
---

# `BlacklistableUpgradeable::blacklist(address(0))` bricks all mint and burn paths across HilToken and StakingVault

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `blacklist(address _account)` performs no parameter validation and silently writes `_blacklisted[address(0)] = true`. ERC-20 `_mint` calls `_update(address(0), to, amount)` and `_burn` calls `_update(from, address(0), amount)`. Both paths are blocked by the `notBlacklisted` guards on `from` and `to` respectively. After one `blacklist(0)` call:

- `Minter::mint → HilToken::mint → _update(address(0), to, amount)` → reverts `UserBlacklisted()`.
- `Minter::redeem → HilToken::burnFrom → _burn → _update(from, address(0), amount)` → reverts.
- `StakingVault::deposit → _mint → _update(address(0), shares_to, shares)` → reverts.
- `StakingVault::claimWithdraw → IHilToken.burn → _update(vault, address(0), amount)` → reverts.

**Recommended Mitigation:** Add `require(_account != address(0), AddressCantBeZero())` at entry of `BlacklistableUpgradeable::blacklist`.

**Syntetika:** Fixed in commit [`cd54186`](https://github.com/SyntetikaLabs/monorepo/commit/cd5418656fbe7872ae8dd57a232c0677e15f242a). Protected addresses will be set during deployment, `address(0)` will be set as protected

**Cyfrin:** Verified.

\clearpage
