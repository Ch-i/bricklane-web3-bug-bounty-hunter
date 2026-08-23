---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-10-cyfrin-boundary-v2-2-0-0
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-10T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md
tags:
- firm:cyfrin
- report:2026-01-10-cyfrin-boundary-v2-2
title: Unvested amount is lost if all users withdraw
vuln_class: []
---

# Unvested amount is lost if all users withdraw

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-10-cyfrin-boundary-v2.2.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-10-cyfrin-boundary-v2.2.md)_

---

**Description:** `sUSBD` permanently locks an initial “burnt” share balance (minted to the vault itself for donation-attack protection). During a vesting period, if all user shares are redeemed/burned such that only the locked shares remain, the remaining unvested rewards continue vesting into `totalAssets()` and are effectively attributed to the locked shares. As a result, rewards that were intended for stakers become permanently unclaimable.

**Impact:** A portion (up to all) of unvested rewards can be irreversibly “lost” if users fully exit during an active vesting period. This will strand reward funds inside the vault, accruing to the locked share balance that cannot be redeemed.

**Proof of Concept:** Add the following test to `test/unit/staking/sUSDB.Withdraw.t.sol`:
```solidity
function test_VestedAmountIsLostIfAllUsersWithraw() public {
    // First set cooldown to 0 to enable direct withdraw/redeem
    vm.prank(operationalAdmin);
    isusbdMgmt.setCooldownDuration(0);

    vm.prank(rewarder);
    isusbd.transferInRewards(100e18);

    // user withdraws after half the vesting period
    vm.warp(block.timestamp + 7 days);

    vm.prank(user1);
    uint256 assets = isusbd.redeem(500e18, user1, user1);

    assertApproxEqAbs(assets, 550e18, 1e18);

    // rest of the vesting period goes
    vm.warp(block.timestamp + 7 days);

    uint256 burntAssets = isusbd.convertToAssets(isusbd.balanceOf(address(isusbd)));

    // rest of the vested amount is vested to the initial burnt shares
    assertApproxEqAbs(burntAssets, 51e18, 1e18);
}
```

**Recommended Mitigation:** Consider one of the following options:

* Maintain a significant protocol deposit at all time (significantly above the locked shares), which will ensure there's always at least one user.
* Add a "sweep" mechanism to sweep the locked shares to the treasury (`if(totalSupply() == 1e18) sweepAssets = convertToAssets(1e18) - 1e18)`)


**Boundary:**
Resolved in [PR#157](https://github.com/boundary-labs/boundary-protocol-ethereum/pull/157) added a check for active stakers in transferInRewards and lowered the initial burnt deposit to 1e12. Additionally, we will initiate and maintain a protocol deposit significantly above the locked shares to ensure there is always at least one staker.

**Cyfrin:** Verified. `transferInRewards` reverts if no stakers.
