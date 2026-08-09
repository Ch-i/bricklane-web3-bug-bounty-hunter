---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-6
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`HilToken` admin blacklisting `TokensHolder` or `StakingVault` in its blacklist
  freezes every vault exit - cross-contract blacklist DoS by a single `HilToken` admin
  key'
vuln_class: []
---

# `HilToken` admin blacklisting `TokensHolder` or `StakingVault` in its blacklist freezes every vault exit - cross-contract blacklist DoS by a single `HilToken` admin key

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** `HilToken` and `StakingVault` each maintain their own `BlacklistableUpgradeable` storage (namespaced per contract). The HilToken blacklister (initially `_initialAdmin` on HilToken deploy) can blacklist ANY address in HilToken's mapping - including protocol-internal addresses like `StakingVault` or `TokensHolder`. Downstream effect:

- `StakingVault::_withdraw` transfers HilToken to `TokensHolder`: `HilToken::_update(vault, tokensHolder, ...)` runs `notBlacklisted(to=tokensHolder)` - if tokensHolder is blacklisted in HilToken, all `redeem`/`withdraw` revert.
- `claimWithdraw` calls `tokensHolder.withdraw(receiver, assets)` which calls `HilToken.transfer`: `_update(tokensHolder, receiver, ...)` runs `notBlacklisted(from=tokensHolder)` - reverts if blacklisted.
- `claimWithdraw` also calls `IHilToken(asset()).burn(...)` when `assets < _initialAssets`; that `_update(stakingVault, 0, ...)` runs `notBlacklisted(from=stakingVault)` - reverts if StakingVault is blacklisted in HilToken.
- `Minter::realizeLosses` calls `HilToken.burnFrom(stakingVault, ...)` - same path; DoS if StakingVault blacklisted.

A single compromised HilToken admin/blacklister key can freeze the entire vault exit surface.

Sources: issuance/src/vault/StakingVault.sol:297-344, 351-388, 571-605; issuance/src/helpers/TokensHolder.sol:34-36.

**Recommended Mitigation:**
- Exclude protocol-internal addresses (vault, tokensHolder, minter) from being blacklistable in HilToken - maintain a hard-coded exclusion list
- Use a single unified blacklist registry shared across HilToken and StakingVault
- Document the operational invariant explicitly: "HilToken admin MUST NOT blacklist the StakingVault or TokensHolder addresses"

**Syntetika:** Fixed in commit [`cd54186`](https://github.com/SyntetikaLabs/monorepo/commit/cd5418656fbe7872ae8dd57a232c0677e15f242a). Protected addresses will be set during deployment

**Cyfrin:** Verified. A list of non-blacklistable addresses introduced.
