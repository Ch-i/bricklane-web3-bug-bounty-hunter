---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-2
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Updating `vestingPeriod` can retroactively reclassify vested rewards as unvested
vuln_class: []
---

# Updating `vestingPeriod` can retroactively reclassify vested rewards as unvested

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** `sUSBD` tracks an active vesting “epoch” using `vestingAmount` and `lastRewardTimestamp`, while `sUSBD::getUnvestedAmount` computes remaining unvested rewards using the current `vestingPeriod`. If `vestingPeriod` is updated after rewards have been transferred in, the vault can retroactively change how much of that epoch is considered “unvested” (even after it was previously fully vested). Since `totalAssets()` is computed as `balanceOf(this) - getUnvestedAmount()`, this can (i) cause `totalAssets()` to underflow and revert when `getUnvestedAmount()` exceeds the vault’s current balance, and/or (ii) temporarily suppress `totalAssets()` without reverting, allowing early redeemers to receive less while later redeemers benefit as the “resurrected” unvested amount decays over time.

**Impact:** * **DoS / broken ERC4626 accounting:** If `getUnvestedAmount() > vaultBalance`, calls depending on `totalAssets()` (and conversions/withdrawals) can revert (underflow) until sufficient time passes.
* **Unfair reward distribution:** If `0 < totalAssets() < vaultBalance`, the share price is temporarily reduced, so redeemers during that window receive fewer assets, while remaining holders later receive more as the same epoch “re-vests,” effectively redistributing rewards based on timing rather than share ownership during the reward period.

**Proof of Concept:** Add the following test to `test/unit/staking/main/sUSBD.GetUnvestedAmount.t.sol`, it shows how changing the vesting period can re-activate vesting and cause DoS when `totalAssets` is called:
```solidity
function test_GetUnvestedAmount_CanResurrectAfterVestingPeriodIncrease_AndMakeTotalAssetsUnderflow()
    public
{
    // Enable direct withdraw/redeem path (so user can exit fully)
    vm.prank(operationalAdmin);
    isusbdMgmt.setCooldownDuration(0);

    vm.prank(operationalAdmin);
    isusbdMgmt.setVestingPeriod(1);

    // Start a vesting epoch
    vm.prank(rewarder);
    isusbd.transferInRewards(REWARD_AMOUNT);

    // Let rewards fully vest under the current vestingPeriod
    vm.warp(block.timestamp + _vault.vestingPeriod());
    assertEq(isusbd.getUnvestedAmount(), 0);

    // User exits, pulling out vested rewards (leaving only the permanently locked shares behind)
    vm.startPrank(user1);
    isusbd.redeem(isusbd.balanceOf(user1), user1, user1);
    vm.stopPrank();
    // Increase vesting period AFTER vesting completed. Because getUnvestedAmount() uses the *current*
    // vestingPeriod with the same vesting epoch state, this can "resurrect" a non-zero unvested amount.
    vm.prank(operationalAdmin);
    isusbdMgmt.setVestingPeriod(uint24(14 days));

    uint256 resurrectedUnvested = isusbd.getUnvestedAmount();
    uint256 vaultBal = IERC20(_vault.asset()).balanceOf(address(isusbd));

    // The problematic condition: unvested becomes larger than the vault's actual balance
    assertGt(resurrectedUnvested, vaultBal);

    // totalAssets() does (balance - unvested) -> underflow panic (0x11)
    vm.expectRevert(stdError.arithmeticError);
    isusbd.totalAssets();
}
```
Together with these two imports:
```diff
+ import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
+ import { stdError } from "forge-std/StdError.sol";
```

**Recommended Mitigation:** Consider setting `vestingAmount = 0` when updating the vesting period:
```diff
    function setVestingPeriod(
        uint24 period
    ) external onlyRole(OPERATIONAL_ADMIN_ROLE) {
        if (period > MAX_VESTING_PERIOD) revert ExceedsMax();
        if (period == 0 && cooldownDuration == 0) revert ZeroCooldownAndPeriod();
        if (getUnvestedAmount() != 0) revert VestingInProgress();

        uint24 oldPeriod = vestingPeriod;
        vestingPeriod = period;
+       vestingAmount = 0;

        emit VestingPeriodUpdated(msg.sender, oldPeriod, period);
    }
```

**Boundary:**
Resolved. Fixed in [PR#181](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/181) as recommended by resetting `vestingAmount` to 0 when updating the vesting period.

**Cyfrin:** Verified. Recommended fix implemented.

\clearpage
