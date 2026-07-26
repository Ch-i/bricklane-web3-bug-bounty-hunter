---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2025-12-24-cyfrin-wannabetv2-v2-0-0-0
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2025-12-24T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md
tags:
- firm:cyfrin
- report:2025-12-24-cyfrin-wannabetv2-v2-0
title: Active and pending bets can be cancelled by anyone
vuln_class: []
---

# Active and pending bets can be cancelled by anyone

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2025-12-24-cyfrin-wannabetv2-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2025-12-24-cyfrin-wannabetv2-v2.0.md)_

---

**Description:** [`Bet::cancel`](https://github.com/gskril/wannabet-v2/blob/d7333369548874cb99e9648ea2424ac1e67cc23f/contracts/src/Bet.sol#L163-L176) allows any address (except the maker) to cancel a bet while it is in the `ACTIVE` or `PENDING` state:

```solidity
/// @dev Anybody can cancel an expired bet and send funds back to each party. The maker can cancel a pending bet.
function cancel() external {
    IBet.Bet memory b = _bet;

    // Can't cancel a bet that's already completed
    if (b.status >= IBet.Status.RESOLVED) {
        revert InvalidStatus();
    } else {
        // Pending or active bets at this point
        // The maker can cancel a pending bet, so block them from cancelling an active bet
        // @audit-issue this only prevents `maker` from cancelling, anyone including the taker can cancel an active bet
        if (b.maker == msg.sender && b.status != IBet.Status.PENDING) {
            revert InvalidStatus();
        }
    }
```

The logic only prevents the maker from cancelling an `ACTIVE` bet or anyone from cancelling after the bet has reached a final state. In practice, this means any arbitrary address (including the `taker`) can cancel both `PENDING` and `ACTIVE` bets at any time.

**Impact:** Allowing any user to cancel a bet enables griefing and, more critically, lets the taker unilaterally back out of a bet they have already accepted. For example, in a sports bet, once the taker observes that their side is likely to lose, they can simply call `cancel()` to unwind the bet and reclaim their stake, undermining the integrity of the betting mechanism.

**Proof of Concept:** Add following test to `BetFactory.t.sol` which shows that the `taker` can cancel a non-expired `ACTIVE` bet:

```solidity
// Anyone can cancel a non-expired ACTIVE bet
function test_ActiveBetCanBeCancelledByAnyone() public {
    // 1. Have the taker accept the bet so it becomes ACTIVE
    vm.startPrank(taker);
    usdc.approve(address(betNoPool), 1000);
    betNoPool.accept();
    vm.stopPrank();

    // Sanity check: bet is ACTIVE
    assertEq(uint(betNoPool.bet().status), uint(IBet.Status.ACTIVE));

    // 2. Warp to a time before resolveBy so the bet is still non-expired
    IBet.Bet memory state = betNoPool.bet();
    vm.warp(uint256(state.resolveBy) - 1);
    assertEq(uint(betNoPool.bet().status), uint(IBet.Status.ACTIVE));

    uint256 makerBalanceBefore = usdc.balanceOf(maker);
    uint256 takerBalanceBefore = usdc.balanceOf(taker);

    // 3. taker cancels the bet
    vm.prank(taker);
    betNoPool.cancel();

    // 4. After cancellation, the bet is marked CANCELLED and funds are refunded
    assertEq(uint(betNoPool.bet().status), uint(IBet.Status.CANCELLED));
    assertEq(usdc.balanceOf(maker) - makerBalanceBefore, 1000);
    assertEq(usdc.balanceOf(taker) - takerBalanceBefore, 1000);
}
```

**Recommended Mitigation:** Consider not allowing anyone to cancel the bet once it's active, alternatively, only allow the judge to cancel active bets.

**WannaBet:** Fixed in commit [cdf3d64](https://github.com/gskril/wannabet-v2/commit/cdf3d649ab818b67e26b82eb241013adbbcdf473).

**Cyfrin:** Verified.
