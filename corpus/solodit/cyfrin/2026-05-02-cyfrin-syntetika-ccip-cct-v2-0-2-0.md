---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-0
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
title: '`StakingVault::withdraw, redeem` silently ignore ERC-4626 `receiver` and `owner`
  parameters - causes fund loss for aggregators'
vuln_class: []
---

# `StakingVault::withdraw, redeem` silently ignore ERC-4626 `receiver` and `owner` parameters - causes fund loss for aggregators

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Both functions override the standard ERC-4626 3-argument signatures but declare `receiver` and `owner` as unnamed parameters and silently use `msg.sender` internally for (1) share burn (via `_redeemTo` / `_withdrawTo` which call `_withdraw(msg.sender, ..., msg.sender, ...)`), (2) cooldown key (`$.cooldowns[msg.sender]`), and (3) later claim authority (`claimWithdraw(receiver)` called by the original redeemer).

ERC-4626 spec requires burning shares from `owner` (spending `msg.sender`'s allowance) and sending assets to `receiver`. Any ERC-4626-compliant aggregator/router (Yearn, ERC-4626 alliance routers, Euler Earn, etc.) that calls `vault.redeem(shares, user, user)` on behalf of a user will either revert with `ERC4626ExceededMaxRedeem` if the aggregator holds no vault shares itself, or silently burn the aggregator's OWN pooled shares keyed to the aggregator rather than to the user - losing funds of other aggregator users and stranding this user's funds in the aggregator's cooldown slot.

The `deposit`/`mint` path correctly honors `receiver`, making the asymmetry particularly dangerous: value enters via the standard interface but cannot leave through it.

Source: `issuance/src/vault/StakingVault.sol:297-344`.

**Impact:** Any ERC-4626 integration loses funds or DoSes. Breaks compatibility with all standard router/aggregator integrations. Future CCT integration (share lock&release) also becomes uncertain since destination chain wrappers typically rely on canonical 4626 semantics.

**Recommended Mitigation:** Either honor the spec - use `receiver` and `owner` with proper `_spendAllowance(owner, msg.sender, shares)` and key cooldowns by `owner` - or remove the 3-arg overrides entirely so the inherited OZ implementations either revert loudly or the contract doesn't advertise 4626 compliance.

**Syntetika:** Fixed in commit [`44fa99e`](https://github.com/SyntetikaLabs/monorepo/commit/44fa99e8c9c2f1a54543a34fd803fbf5cd962c2b)

**Cyfrin:** `claimWithdraw` permanently reverts after cooldown elapses when earlyExitEnabled = true

When `earlyExitEnabled = true` and a user's cooldown has fully elapsed, `claimWithdraw` falls into the `else if ($.earlyExitEnabled)` branch (not the `!earlyExitEnabled && elapsed` branch). `getEarlyExitAmount` returns `(fee=0, netWithdraw=assets)`. The second `_withdraw(... earlyExitFee=0, earlyExitSharesFee=0)` then hits `if (assets < $.minAssetsAmount) revert AmountBelowLimit()` at line 668. With `minAssetsAmount = 1000` (deployment default), every elapsed cooldown is unclaimable while `earlyExitEnabled` is on. Users must either pay the early-exit fee before cooldown ends, or wait for admin to toggle the flag off.

Fix: add `block.timestamp >= userCooldown.cooldownEnd` check before the early-exit branch, OR skip the second `_withdraw` when `earlyExitFee == 0`.

**Syntetika:** Fixed in commit [`6fdc89d`](https://github.com/SyntetikaLabs/monorepo/commit/6fdc89d0a0d1da3602100fadc71750779de0a213)

**Cyfrin:** In the cooldown path: `_transfer` is OZ's internal ERC-20 function, it moves balances directly with no allowance check. If `msg.sender != owner`, the shares are transferred from `owner` to `TokensHolder` without owner's consent. Anyone can call vault.redeem(bob_shares, anyAddress, bob) to force Bob's shares into cooldown and reset his cooldown timer.

The fix should add an explicit allowance check at the top of the cooldown branch:
```solidity
if (msg.sender != owner) {
    _spendAllowance(owner, msg.sender, shares);
}
```
before the `_transfer` call, matching what OZ's `_withdraw` does in the no-cooldown path.

**Syntetika:** Fixed in commit [`f221196`](https://github.com/SyntetikaLabs/monorepo/commit/f221196eb96025e5d2dc5f09e500eee3c34b461c)

**Cyfrin:** When `earlyExitEnabled = true` and a user exits early late in their cooldown window, `earlyExitFee` can be non-zero but smaller than `minAssetsAmount`. The new guard `if (earlyExitFee >= $.minAssetsAmount)` skips the second `_withdraw`, but `earlyExitSharesFee` shares are already excluded from the first burn, they sit in `TokensHolder` permanently with no cooldown record pointing to them.

Fix (Option A): Burn `earlyExitSharesFee` unconditionally; only gate the asset transfer on `earlyExitFee >= $.minAssetsAmount`.
Fix (Option B): When the fee would be below the floor, treat it as zero, set `netWithdraw = assets` and burn all underlyingShares.

**Syntetika:** Fixed in commit [`34eb001`](https://github.com/SyntetikaLabs/monorepo/commit/34eb00140d37d15e86f42cf8e3f385d20d95c2e4)
