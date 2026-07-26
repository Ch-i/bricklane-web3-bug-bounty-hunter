---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-16
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`HilToken::_update` and `StakingVault::_update` check blacklist status of
  `address(0)`'
vuln_class: []
---

# `HilToken::_update` and `StakingVault::_update` check blacklist status of `address(0)`

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Both `_update` overrides check blacklist status of every address involved in a token movement, `from`, `to`, and `msg.sender`, without first excluding the ERC-20 sentinel `address(0)`.

`ERC20::_mint` calls `_update(address(0), to, amount)`: `from` is `address(0)`.
`ERC20::_burn` calls `_update(from, address(0), amount)`: `to` is `address(0)`.

**HilToken** (non-owner path, `issuance/src/token/HilToken.sol:212-217`):
```solidity
require(
    !_isBlacklisted(from) &&   // ← address(0) checked during _mint
    !_isBlacklisted(to) &&     // ← address(0) checked during _burn
    !_isBlacklisted(msg.sender),
    UserBlacklisted()
);
```

**StakingVault** (`issuance/src/vault/StakingVault.sol:575-577`):
```solidity
notBlacklisted(from)      // ← address(0) checked during share mint (deposit)
notBlacklisted(to)        // ← address(0) checked during share burn (withdraw)
notBlacklisted(msg.sender)
```

`address(0)` is not a real participant — it holds no tokens, has no signing key, and cannot be a counterparty in any compliance context. Checking it against the blacklist is semantically meaningless and creates an avoidable attack surface: any mechanism that writes `_blacklisted[address(0)] = true` (whether via the `blacklist()` function directly, a storage collision, or an upgrade bug) silently bricks every mint and burn across both contracts simultaneously.

**Mitigation:**

Guard both `from` and `to` blacklist checks with a non-zero sentinel exclusion:

**HilToken:**
```solidity
if (msg.sender != owner()) {
    require(
        (from == address(0) || !_isBlacklisted(from)) &&
        (to   == address(0) || !_isBlacklisted(to))   &&
        !_isBlacklisted(msg.sender),
        UserBlacklisted()
    );
}
```

**StakingVault:**
```solidity
function _update(address from, address to, uint256 amount)
    internal override
    notBlacklisted(msg.sender)
{
    if (from != address(0)) _requireNotBlacklisted(from);
    if (to   != address(0)) _requireNotBlacklisted(to);
    super._update(from, to, amount);
}
```

This aligns with standard compliance-token practice (USDC, EUROC) where `address(0)` is implicitly excluded from blacklist checks because it participates only as an ERC-20 accounting sentinel, never as a real token holder.

**Syntetika:** Fixed in commit [`6ced19`](https://github.com/SyntetikaLabs/monorepo/commit/6ced196a48548e80cc85883f8c23107d96dff292)

**Cyfrin:** Verified.

\clearpage
