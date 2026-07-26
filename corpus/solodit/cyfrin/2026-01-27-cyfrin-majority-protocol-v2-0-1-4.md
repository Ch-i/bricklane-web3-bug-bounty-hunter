---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-1-4
ingested_at: '2026-07-26T07:14:09Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: High
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: If multiple users call `DefaultSession::assertResults` all but the first caller
  lose their bonds
vuln_class: []
---

# If multiple users call `DefaultSession::assertResults` all but the first caller lose their bonds

_Section severity (from Solodit section header): High_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** The `assertResults` is a permissionless function that allow anyone to assert a result for a `gameId` (sessionId):

```solidity
function assertResults(
        uint256 sessionId,
        string calldata resultCid,
        address[] calldata proposedWinners,
        uint256[] calldata totalXPs,
        uint256[] calldata totalTimes
    ) external returns (bytes32 assertionId) {
        require(SessionManager(sessionManager).getSessionState(sessionId) == SessionState.Ended, GameNotEnded());
        return assertDataFor(
            sessionId, resultCid, resolutionGitRepoAtCommitHash, proposedWinners, totalXPs, totalTimes, msg.sender
        );
    }
```

Users that call this function have to pay a usdc bond of 250 dollars, see [minimum bonds value](https://docs.uma.xyz/resources/approved-collateral-types).

```solidity
 function assertDataFor(
        uint256 sessionId,
        string calldata resultCid,
        string memory resolutionGitRepoAtCommitHash,
        address[] calldata winners,
        uint256[] calldata totalXPs,
        uint256[] calldata totalTimes,
        address asserter
    ) internal returns (bytes32 assertionId) {
        asserter = asserter == address(0) ? msg.sender : asserter;
        uint256 bond = optimisticOracle.getMinimumBond(address(usdc)); /
        usdc.safeTransferFrom(msg.sender, address(this), bond);  <--------
        usdc.forceApprove(address(optimisticOracle), bond); <-------
}
```

The problem is that this function is not restricting users to call `assertResults` more than once for the same `sessionId` with that being say lets explore what would happen if `assertResults` is called twice for the same `sessionId`, `winners`, `totalXPs` and `TotalTimes` ; note that since the `assertResults` function is permissionless it can naturally be called twice by two different users at the same time:

1. A game has ended
2. User A call `assertResults` passing the session ID and the correct values.
3. User B didn't notice that that user A already call `assertResults` and call again `assertResults`
4. User A true is resolver positive and the `recordResults` function is called setting ` winners[sessionId] = assertion.winners;`
5. User B assertion is resolved positive, the oracle call revert in `recordResults` making the user loss his funds

```solidity
 function recordResults(uint256 sessionId, bytes32 assertionId) public {

        require(SessionManager(sessionManager).getSessionState(sessionId) == SessionState.Ended, GameNotEnded());
        require(
            sessionId == assertions[assertionId].sessionId,
            SessionIdMismatch(sessionId, assertions[assertionId].sessionId)
        );
        require(assertions[assertionId].resolved, AssertionNotInitialized(assertionId));
        require(winners[sessionId].length == 0, WinnersAlreadyRecorded(sessionId));
        ...

        winners[sessionId] = assertion.winners;
    }
```

Note that the UMA protocol recommends [don't revert in the callback](https://github.com/UMAprotocol/protocol/blob/6a23be19d8a0dbee4475db9ff52ce4d9572212b5/packages/core/contracts/optimistic-oracle-v3/implementation/OptimisticOracleV3.sol#L122):
```
recipient _must_ implement these callbacks and not revert or the assertion resolution will be blocked.
```

**Impact:** If `assertResults` is called more than once by different users just the first caller will recover their bond; the other users end up losing their money.

**Proof of Concept:** Run the next proof of concept in `file:test/session/DefaultSession.sol`
```solidity
 function test_RecordResults_double() public { //@audit
        // Mock SessionManager to return Ended state
        vm.mockCall(
            sessionManager, abi.encodeCall(SessionManager.getSessionState, gameId), abi.encode(SessionState.Ended)
        );

        string memory resultCid = "QmTestResultCID";
        address[] memory proposedWinners = new address[](2);
        proposedWinners[0] = player1;
        proposedWinners[1] = player2;

        uint256[] memory totalXPs = new uint256[](2);
        totalXPs[0] = 200;
        totalXPs[1] = 150;

        uint256[] memory totalTimes = new uint256[](2);
        totalTimes[0] = 30;
        totalTimes[1] = 45;

        vm.mockCall(
            optimisticOracle,
            abi.encodeWithSelector(OptimisticOracleV3Interface.assertTruth.selector),
            abi.encode(keccak256("assertionId43"))
        );
        bytes32 assertionId =
            defaultSession.assertResults(gameId, resultCid, proposedWinners, Solarray.uint256s(200, 150), totalTimes);

        vm.mockCall(
            optimisticOracle,
            abi.encodeWithSelector(OptimisticOracleV3Interface.assertTruth.selector),
            abi.encode(keccak256("assertionId44"))
        );
        bytes32 assertionIdtwo =
            defaultSession.assertResults(gameId, resultCid, proposedWinners, Solarray.uint256s(200, 150), totalTimes); //second assertion with the same values

        // 2. Call the callback to mark the assertion as resolved
        vm.prank(address(optimisticOracle));
        defaultSession.assertionResolvedCallback(assertionId, true);

        vm.startPrank(address(optimisticOracle));
        vm.expectRevert();
        defaultSession.assertionResolvedCallback(assertionIdtwo, true);
    }
```

**Recommended Mitigation:** Either prevent multiple in-process assertions for the same `sessionId`, or just return in the callback without reverting if it was already processed.

**Majority Games:**
Fixed in commit [4c5483f](https://github.com/Engage-Protocol/engage-protocol/commit/4c5483fd6f39b49f2fcd93055151244b4b6cd262) by returning in the callback without reverting if the assertion has already been processed.

**Cyfrin:** Verified.

\clearpage
