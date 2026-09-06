---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-8
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
title: User can set their answer's probability value to `uint16.max`, manipulating
  `result.probabilityAverage` in their favor
vuln_class: []
---

# User can set their answer's probability value to `uint16.max`, manipulating `result.probabilityAverage` in their favor

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** In `SPBinaryPrompt.sol`, users commit an `answer` and a `probability`. When this value is revealed, the `revealReaction` function does not check if the probability exceeds 10,000 (which should be the maximum value based on how the `getScore` function uses probability).

```solidity
function revealReaction(
        uint256 _gameId,
        uint256 _questionId,
        bytes calldata _selection,
        uint256 salt,
        address _user
    ) external {
        (bool answer, uint16 probability) = abi.decode(_selection, (bool, uint16));
        require(
            revealedQuestions[_questionId].sessionManager == msg.sender,
            OnlySessionManager(revealedQuestions[_questionId].sessionManager, msg.sender)
        );
        Reaction storage r = reactions[_questionId][_user];
        require(r.baseReaction.timestamp != 0, AnswerNotCommitted(_user, _gameId, _questionId));
        require(!r.baseReaction.revealed, AnswerAlreadyRevealed(_user, _gameId, _questionId));
        require(
            keccak256(abi.encodePacked(_gameId, _questionId, answer, probability, salt)) == r.baseReaction.commit,
            RevealMismatch(_gameId, _questionId, answer, probability, salt, r.baseReaction.commit)
        );

        r.answer = answer;
        r.probability = probability;

        r.baseReaction.revealed = true;
        ResultAggregate storage result = resultAggregates[_questionId];
        result.respondents++;
        result.answerTotal += answer ? PRECISION : 0;
        result.probabilityTotal += probability; <-------
        result.answerAverage = result.answerTotal / result.respondents;
        result.probabilityAverage = result.probabilityTotal / result.respondents; <------
        emit AnswerRevealed(_gameId, _questionId, _user, answer, probability);
    }
```

As shown, the individual probability is used to calculate the `probabilityAverage`, which is a critical value in this strategy because it is used to compute the score that determines a user’s results.

**Impact:** A malicious user can manipulate the `probabilityAverage` to improve their score, potentially securing a higher ranking among winners.

**Proof of Concept:** Run the next proof of concept in `test/prompt/SPBinaryPromptTest.t.sol`:

```solidity
function test_revealReaction_Success_full_proability() public {
        _createQuestion();

        vm.warp(block.timestamp + 100);

        bytes32 commit = keccak256(abi.encodePacked(gameId, questionId, true, int16(5000), uint256(type(uint16).max)));

        vm.prank(mockSessionManager);
        prompt.commitReaction(gameId, questionId, commit, user0);

        vm.warp(block.timestamp + 100);

        vm.prank(mockSessionManager);
        prompt.revealReaction(gameId, questionId, abi.encode(true, int16(5000)), type(uint16).max, user0);
    }
```

**Recommended Mitigation:** Consider capping probability at 10,000 if a user commits a higher value:

```diff
function revealReaction(
        uint256 _gameId,
        uint256 _questionId,
        bytes calldata _selection,
        uint256 salt,
        address _user
    ) external {
        (bool answer, uint16 probability) = abi.decode(_selection, (bool, uint16));
        require(
            revealedQuestions[_questionId].sessionManager == msg.sender,
            OnlySessionManager(revealedQuestions[_questionId].sessionManager, msg.sender)
        );
        Reaction storage r = reactions[_questionId][_user];
        require(r.baseReaction.timestamp != 0, AnswerNotCommitted(_user, _gameId, _questionId));
        require(!r.baseReaction.revealed, AnswerAlreadyRevealed(_user, _gameId, _questionId));
        require(
            keccak256(abi.encodePacked(_gameId, _questionId, answer, probability, salt)) == r.baseReaction.commit,
            RevealMismatch(_gameId, _questionId, answer, probability, salt, r.baseReaction.commit)
        );
+     if (probability > PRECISION ) { probability = PRECISION; }

        r.answer = answer;
        r.probability = probability;

        r.baseReaction.revealed = true;
        ResultAggregate storage result = resultAggregates[_questionId];
        result.respondents++;
        result.answerTotal += answer ? PRECISION : 0;
        result.probabilityTotal += probability;
        result.answerAverage = result.answerTotal / result.respondents;
        result.probabilityAverage = result.probabilityTotal / result.respondents;
        emit AnswerRevealed(_gameId, _questionId, _user, answer, probability);
    }
```

**Majority Games:**
Fixed in commit [2eaae4d](https://github.com/Engage-Protocol/engage-protocol/commit/2eaae4d5a6213f9728d04c96b346c28b3a618c3c).

**Cyfrin:** Verified.

\clearpage
