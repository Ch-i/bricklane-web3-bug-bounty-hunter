---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-9
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: '`StakingVault::redeem, withdraw` missing zero-output guard in no-cooldown
  path'
vuln_class: []
---

# `StakingVault::redeem, withdraw` missing zero-output guard in no-cooldown path

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** Both `redeem` and `withdraw` contain an explicit zero-output guard — but only in the cooldown branch. When `cooldownDuration == 0` both functions return immediately from their internal helper, bypassing the check entirely.

`redeem` (lines 304–305 vs. 312–314):
```solidity
if (_cooldownDuration == 0) {
    return _redeemTo(shares, msg.sender); // no zero-assets check on return value
}
// cooldown path:
assets = _redeemTo(shares, address($.tokensHolder));
if (assets == 0) { revert ZeroAmount(); } // guard present here only
```

`withdraw` (lines 329–330 vs. 337–339) is symmetric: `return _withdrawTo(assets, msg.sender)` with the `if (shares == 0) revert ZeroAmount()` guard only in the cooldown branch.

`_redeemTo` (line 547) checks `shares > 0` on the input but not the output. `previewRedeem` uses floor division — `shares.mulDiv(totalAssets + 1, totalSupply + 10**offset, Rounding.Floor)` — so for a small `shares` value against a high share price, `assets` rounds to zero. The internal `_withdraw` guard at line 589 (`if (assets < $.minAssetsAmount) revert AmountBelowLimit()`) is the only remaining backstop, but `minAssetsAmount` is configurable to zero via `setMinAssetsAmount` with no lower-bound enforcement.

The result: in a no-cooldown vault with `minAssetsAmount = 0`, a user can call `redeem(dustShares)`, burn their shares, and receive zero assets in return, with no revert and only a misleading `Unstaked(msg.sender, 0)` event.

Source: `issuance/src/vault/StakingVault.sol:297-340`, `543-557`.

**Impact:** Dust share amounts can be silently burned for zero assets in the no-cooldown configuration. The behaviour is inconsistent with the cooldown path (which reverts on zero output) and inconsistent with the `ZeroAmount` error the contract otherwise uses to signal this condition. No direct attacker profit; the burned shares benefit remaining stakers marginally through increased share price.

**Recommended Mitigation:** Apply the zero-output check before returning in both no-cooldown branches:

```solidity
if (_cooldownDuration == 0) {
    assets = _redeemTo(shares, msg.sender);
    if (assets == 0) revert ZeroAmount();
    return assets;
}
```

```solidity
if ($.cooldownDuration == 0) {
    shares = _withdrawTo(assets, msg.sender);
    if (shares == 0) revert ZeroAmount();
    return shares;
}
```

**Syntetika:** Fixed in commit [`5c0f783`](https://github.com/SyntetikaLabs/monorepo/commit/5c0f7835ae935ba7f77b4c0520002042d3ce6531)

**Cyfrin:** Verified.
