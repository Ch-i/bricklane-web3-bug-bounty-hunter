---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-05-02-cyfrin-syntetika-ccip-cct-v2-0-2-10
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-05-02T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md
tags:
- firm:cyfrin
- report:2026-05-02-cyfrin-syntetika-ccip-cct-v2-0
title: Fully-vested yield becomes unvested on vesting period update
vuln_class: []
---

# Fully-vested yield becomes unvested on vesting period update

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-05-02-cyfrin-syntetika-ccip-cct-v2.0.md)_

---

**Description:** The `Distributor::updateTimelock` function allows the admin to update the vesting duration. However, the function neither blocks changes during an active vesting cycle nor does it reset `vestingAmount` after the cycle has ended.

If the admin updates the vesting period during an active cycle or after rewards have fully vested, the `StakingVault::getUnvestedAmount` function will recompute vesting using the new `vestingPeriod`, making already vested rewards becomes unvested again and reduce `StakingVault::totalAssets`.

```solidity
        uint256 deltaT;
        unchecked {
            deltaT = (vestingPeriod - timeSinceLastDistribution);
        }

        return (deltaT * $.vestingAmount) / vestingPeriod;
```

**Impact:** The bug causes several economic issues for the vault:
1. Sudden share price crash: The ERC4626 share price is derived from `totalAssets`. When vested yield suddenly becomes unvested again, the asset value drops immediately.
2. Direct user loss: All vault share holders lose value. Users redeeming immediately after the update (due to transaction order in mempool) receive fewer assets because the contract effectively removes part of their already-earned yield.
3. Arbitrary opportunity: An attacker can withdraw at the high share price before the admin update, followed by a deposit at the deflated price.

**Proof of Concept:** Let's take an example:
 - Assume initially, `vestingAmount = 3600` and `vestingPeriod = 3600s` (1 hour).
 - At T = 3601s, the vesting cycle is considered complete. Due to this, `getUnvestedAmount` returns 0 and `totalAssets` includes the 3600 tokens.
 - Admin calls `updateTimelock(7200)` to extend the period from 1 hour to 2 hours.
 - `getUnvestedAmount` calculates unvested amount using the old `vestingAmount` (3600) and new period (7200).
 - $$Unvested = \frac{(7200 - 3601) \times 3600}{7200} = 1799.5$$
 - `totalAssets` instantly drops by ~1800 tokens.

**Recommended Mitigation:** Consider implemented the following logical changes in `Distributor::updateTimelock:
```diff
 /// @notice Updates the time lock duration.
    function updateTimeLock(
        uint256 _timeLock
    ) external onlyRole(DEFAULT_ADMIN_ROLE) {
        require(_timeLock > 0, InvalidTimeLock());

+      if (getUnvestedAmount() > 0) {
+          revert StillVesting();
+       }

+      if (vestingAmount > 0) vestingAmount = 0

        DistributorStorage storage $ = _getDistributorStorage();
        $.timeLock = _timeLock;
        emit TimeLockUpdated(_timeLock);
    }
```

**Syntetika:** Fixed in commit [`dee5502`](https://github.com/SyntetikaLabs/monorepo/commit/dee550210a524bf32d7b765f1b1647c275894236)

**Cyfrin:** The fix added:

```solidity
if (IStakingVault($.minter.stakingVault()).getUnvestedAmount() > 0) {
    revert StillVesting();
}
```

This correctly blocks updates **during** an active vesting cycle. But the recommended mitigation also asked for resetting `vestingAmount` to 0 when the cycle has already **fully** vested, and that part was not implemented.

The vulnerability still exists: if yield fully vests (`timeSinceLastDistribution >= timeLock`, so `getUnvestedAmount() == 0`), the check passes. Then if timeLock is increased to a larger value, `timeSinceLastDistribution < newTimeLock`, and the stale `$.vestingAmount` in vault storage produces spurious unvested yield again.

Example from the original report: `vestingAmount = 3600`, old `timeLock = 3600s`. At T+3601 everything is vested, `getUnvestedAmount() == 0`. Admin updates `timeLock = 7200`. Immediately, `getUnvestedAmount()` returns ~1799 and share price drops. This window persists until the next distribution resets `vestingAmount`.

The active-vesting guard is now in place but the post-vesting stale state is not handled. The second line of the recommended mitigation, resetting `vestingAmount` to 0 in the vault before changing the timeLock, is still missing.

**Syntetika:** Fixed in commit [`602c864`](https://github.com/SyntetikaLabs/monorepo/commit/602c864f73e800fd24c25ebc3b8dad78e70c9db0)

**Cyfrin:** Verified. The fix adds a `resetVesting()` function and wires it into the `updateTimeLock` flow. The full call chain: `Distributor::updateTimeLock -  Minter::resetVesting() -> StakingVault::resetVesting()` which sets `$.vestingAmount = 0`.
