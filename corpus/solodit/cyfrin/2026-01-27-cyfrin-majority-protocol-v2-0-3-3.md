---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-3
ingested_at: '2026-09-06T08:49:48Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`SessionManager::cancelGameIfCreatorMissing, endGame` could revert due to
  out of gas if there are too many question in a game'
vuln_class: []
---

# `SessionManager::cancelGameIfCreatorMissing, endGame` could revert due to out of gas if there are too many question in a game

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Since there are no restrictions on the number of questions a game can support, a game could have so many questions that it causes `SessionManager::cancelGameIfCreatorMissing, endGame` to revert due to out-of-gas errors.

* `endGame` iterates over all questions:
```solidity
 function endGame(uint256 _gameId) external onlyState(_gameId, SessionState.Ongoing) {
        require(block.timestamp >= games[_gameId].endTime, GameIsNotEnded(games[_gameId].endTime, block.timestamp));
        uint256[] storage questions = gameQuestions[_gameId];
        for (uint256 i = 0; i < questions.length; i++) {
            require(_isRevealed(questions[i]), QuestionNotRevealed(_gameId, questions[i]));
        } <-----------
        games[_gameId].state = SessionState.Ended;
        emit GameEnded(_gameId);
    }
```

* so does `cancelGameIfCreatorMissing`:
```solidity
  function cancelGameIfCreatorMissing(uint256 _gameId) external {
        require(
            games[_gameId].state != SessionState.Cancelled,
            InvalidGameState(SessionState.Cancelled, games[_gameId].state)
        );
        require(
            games[_gameId].state != SessionState.Concluded,
            InvalidGameState(SessionState.Concluded, games[_gameId].state)
        );
        require(block.timestamp >= games[_gameId].endTime, GameIsNotEnded(games[_gameId].endTime, block.timestamp));
        uint256[] storage questions = gameQuestions[_gameId];
        for (uint256 i = 0; i < questions.length; i++) { <-------

            if (!_isRevealed(questions[i])) {
                games[_gameId].state = SessionState.Cancelled;
                emit GameCancelled(_gameId);
                return;
            }
        }
        revert GameWaitingForConclusion(_gameId);
    }
```

**Impact:** `SessionManager::cancelGameIfCreatorMissing, endGame` could revert if there are too many questions in a game.

* If `endGame` cannot complete, users and the creator lose their funds and fees
* If `cancelGameIfCreatorMissing` reverts, users lose their funds if the creator is missing

**Recommended Mitigation:** Limit the number of questions in a game.

**Majority Games:**
Fixed in commit [cb88233](https://github.com/Engage-Protocol/engage-protocol/commit/cb8823378ef74d688ff15eefb7b6ac0d2b0e5bc2).

**Cyfrin:** Verified.
