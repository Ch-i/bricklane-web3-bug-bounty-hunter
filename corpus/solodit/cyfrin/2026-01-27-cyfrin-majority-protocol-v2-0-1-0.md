---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-1-0
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Impossible for user to get refund after re-joining a rescheduled game which
  is subsequently cancelled
vuln_class: []
---

# Impossible for user to get refund after re-joining a rescheduled game which is subsequently cancelled

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Impossible for user to get refund after re-joining a rescheduled game which is subsequently cancelled.

**Impact:** The user's fee for joining the game is permanently locked inside the immutable `SessionManager` contract.

**Proof of Concept:** Add the PoC to `SessionManagerLeaveGame.t.sol`:
```solidity
function test_gameRescheduled_Leave_JoinAgain_GameCancelled_UserRefundReverts() public {
    // create a game
    uint256 timeAfterRescheduling = sessionManager.minimumRescheduleTime();
    _createGame();
    uint256 rescheduleDelta = type(uint256).max - sessionManager.getStartTime(1);

    // user joins the game
    uint256 gameId = 1;
    uint256 gameFee = 10 ether;
    address user = contestants[0];
    uint256 startTime = sessionManager.getStartTime(gameId);
    vm.startPrank(user);
    TestUSDC(usdc).approve(address(sessionManager), gameFee);
    sessionManager.joinGame(gameId);
    vm.stopPrank();

    // game gets rescheduled
    sessionManager.rescheduleGame(1, startTime + rescheduleDelta);
    vm.warp(block.timestamp + timeAfterRescheduling);

    // user leaves rescheduled game
    vm.prank(user);
    sessionManager.leaveRescheduledGame(gameId);

    // user got refunded the game fee
    assertEq(TestUSDC(usdc).balanceOf(user), gameFee);
    assertEq(TestUSDC(usdc).balanceOf(address(sessionManager)), 0 ether);

    // user decides to re-join the game
    vm.startPrank(user);
    TestUSDC(usdc).approve(address(sessionManager), gameFee);
    sessionManager.joinGame(gameId);
    vm.stopPrank();

    // user decides to leave again; impossible
    vm.expectRevert(); // AlreadyRefunded(0xd52E4d00E363cB91d9051fBFDC80c292a1da630B, 1)]
    vm.prank(user);
    sessionManager.leaveRescheduledGame(gameId);

    // game is cancelled
    sessionManager.cancelGame(gameId);

    // impossible for user to get a refund!
    vm.expectRevert(); // AlreadyRefunded(0xd52E4d00E363cB91d9051fBFDC80c292a1da630B, 1)]
    vm.prank(user);
    sessionManager.refundCancelledGame(gameId);

    // user's game fee is permanently stuck in the session manager contract!
    assertEq(TestUSDC(usdc).balanceOf(user), 0);
    assertEq(TestUSDC(usdc).balanceOf(address(sessionManager)), gameFee);
}
```

**Recommended Mitigation:** In `DepositManager::_payEntryFee` add this:
```solidity
// reset user refunded status when joining the game; this allows
// users to get refunded if they rejoin a game which later gets cancelled
if(hasRefunded[gameId][player]) hasRefunded[gameId][player] = false;
```

**Majestic Games:**
Fixed in commit [3ac5654](https://github.com/Engage-Protocol/engage-protocol/commit/3ac565495df69ba8936be9d3d91a77eeb639b366) by not allowing users who have been refunded to rejoin the same game.

**Cyfrin:** Verified.
