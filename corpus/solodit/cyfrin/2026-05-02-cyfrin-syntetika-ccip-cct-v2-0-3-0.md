---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-3-0
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`StakingVault::_withdraw` last-user branch reverts with `ERC20InvalidReceiver`
  when owner is renounced to zero - DoS of last-user exit during vesting window'
vuln_class: []
---

# `StakingVault::_withdraw` last-user branch reverts with `ERC20InvalidReceiver` when owner is renounced to zero - DoS of last-user exit during vesting window

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** When a withdrawal makes `totalSupply() - shares == DEAD_SHARES` (last real user exiting) and unvested yield still exists, `_withdraw` sweeps the entire unvested amount to `owner()`:

```solidity
if (totalSupply() - shares == DEAD_SHARES) {
    uint256 remainingUnvested = getUnvestedAmount();
    if (remainingUnvested > 0) {
        $.vestingAmount = 0;
        $.lastDistributionTimestamp = 0;
        IERC20(asset()).safeTransfer(owner(), remainingUnvested);
    }
}
```

`StakingVault` inherits `OwnableUpgradeable` via `BlacklistableUpgradeable` without overriding `renounceOwnership`. Neither function has a 2-step acceptance pattern (`Ownable2StepUpgradeable` exists in OZ but is not used). After an honest admin `renounceOwnership()` (plausible decentralization move), `owner() == address(0)`:

1. Distribution fires; `vestingAmount > 0`, `getUnvestedAmount() > 0`.
2. Last real staker attempts to exit: `redeem(allShares)` -> `_withdraw` hits the `totalSupply() - shares == DEAD_SHARES` branch -> `safeTransfer(owner()==0, remainingUnvested)` -> reverts with `ERC20InvalidReceiver(address(0))`.
3. Last staker DoSed until `getUnvestedAmount() == 0` (full `vestingPeriod` decay).

Sources: inherited OZ OwnableUpgradeable; StakingVault.sol:598-605.

Note: the generic `transferOwnership`/`renounceOwnership` inherited behavior is reported as a Centralization disclosure (intended OZ `Ownable` semantics). The subcase reported here is the honest-admin-triggered DoS path on `_withdraw`.

**Impact:** Permanent repeating DoS of last-user exit whenever unvested yield exists after an honest `renounceOwnership`. User must either wait for `getUnvestedAmount() == 0` (up to `vestingPeriod`) or leave >= 1 wei of shares behind (may conflict with `minAssetsAmount`).

**Recommended Mitigation:**
- Override `renounceOwnership()` to revert - the StakingVault first-deposit path and `_withdraw` last-user sweep depend on a live owner
- Guard the transfer: `if (remainingUnvested > 0 && owner() != address(0)) { safeTransfer(owner(), remainingUnvested); }` and leave `remainingUnvested` in the vault otherwise
- Migrate `BlacklistableUpgradeable` to `Ownable2StepUpgradeable` so ownership transfer requires explicit `acceptOwnership`
- Bind `owner()` strictly to `DEFAULT_ADMIN_ROLE`: override every `onlyOwner` call-site to require `onlyRole(DEFAULT_ADMIN_ROLE)` on the same caller, OR drop `onlyOwner` in favor of role-gated modifiers

**Syntetika:** Fixed in commit [`536b5d3`](https://github.com/SyntetikaLabs/monorepo/commit/536b5d39ef011442ca88f036be7d76767e7e341a)

**Cyfrin:** Verified. `renounceOwnership` reverts.
