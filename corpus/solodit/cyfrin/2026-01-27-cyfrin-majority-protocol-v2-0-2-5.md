---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-5
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Game creator can call `TriviaChoicePrompt::revealSolutions` before the `reactionDeadline`
  or end of game, griefing players from submitting answers while still retaining player
  entry fees
vuln_class: []
---

# Game creator can call `TriviaChoicePrompt::revealSolutions` before the `reactionDeadline` or end of game, griefing players from submitting answers while still retaining player entry fees

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `TriviaChoicePrompt::revealSolutions` calls `_revealSolutions` which doesn't validate that `reactionDeadline` has expired. This causes `TriviaChoicePrompt::commitReaction` to revert when users try to submit answers:
```solidity
 function commitReaction(uint256 _gameId, uint256 _questionId, bytes32 _commit, address _user) external {
        require(revealedAt[_questionId] != 0, QuestionNotRevealed(_questionId));
        require(
            revealedQuestions[_questionId].sessionManager == msg.sender,
            OnlySessionManager(revealedQuestions[_questionId].sessionManager, msg.sender)
        );
        require(solutionRevealedAt[_questionId] == 0, SolutionAlreadyRevealed(_questionId)); <------
        require(
            revealedAt[_questionId] + revealedQuestions[_questionId].reactionDeadline > block.timestamp,
            ReactionDeadlinePassed(_user, _questionId)
        );
        Reaction storage r = reactions[_questionId][_user];
        require(r.baseReaction.timestamp == 0, AnswerAlreadyCommitted(_user, _gameId, _questionId));

        r.baseReaction.commit = _commit;
        r.baseReaction.timestamp = block.timestamp;

        emit AnswerCommitted(_gameId, _questionId, _user, _commit);
    }
```

**Impact:** A malicious game creator can immediately reveal solutions, preventing users from submitting answers and earning xp. The game creator can still keep the users' entry fees, griefing users.

**Proof of Concept:** Run this test in `test/prompt/TriviaChoicePropmt.t.sol`

```solidity
 function test_solution_as_soon_as_reveledQuestion() public {
        triviaChoice.setRevealedQuestions();
        triviaChoice.revealSolutions(
            1, Solarray.uint256s(1), Solarray.bytess(abi.encode(uint16(1))), Solarray.uint256s(1234)
        );

        vm.expectRevert(abi.encodeWithSelector(TriviaChoicePrompt.SolutionAlreadyRevealed.selector, 1));
        triviaChoice.commitReaction(1, 1, keccak256(abi.encode(uint16(1))), address(this));
    }
```

**Recommended Mitigation:** Don't allow the game creator to call `revealSolution` until the game has end; you can use the games mapping in the session manager  `require(sessionManager.games(_gameId).state = SessionState.Ended)`.

**Majority Games:**
Fixed in commit [4d3f8b5](https://github.com/Engage-Protocol/engage-protocol/commit/4d3f8b5be490bdba368d3d5e961ba3e678dcad9e).

**Cyfrin:** Verified. A different fix was chosen which is actually quite an elegant solution that removes the incentive for this the griefing attack because creators can't reveal solutions early without blocking their own ability to conclude the game, distribute rewards and claim their fees.
