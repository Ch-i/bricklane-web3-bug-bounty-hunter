---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-2
ingested_at: '2026-05-15T13:52:11Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Incorrect `recordResult` recorded for each question in `recordResults`
vuln_class: []
---

# Incorrect `recordResult` recorded for each question in `recordResults`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** When an assertion is resolved the UMA oracle makes a call back to `DefaultSession::assertionResolvedCallback` if the assertion was truthful, it calls `recordResults`:
```solidity
function recordResults(uint256 sessionId, bytes32 assertionId) public {
        ...
        uint256[] memory questionIds = SessionManager(sessionManager).getQuestionsForGame(sessionId);

        for (uint256 i = 0; i < assertion.winners.length; ++i) {
            address winner = assertion.winners[i]; //@audit how many winners could be?
            for (uint256 j = 0; j < questionIds.length; ++j) {
                (, address promptStrategy) = SessionManager(sessionManager).questionCommitment(questionIds[j]);
                IPromptStrategy(promptStrategy).recordResult(
                    questionIds[j], winner, assertion.totalXPs[i], assertion.totalTimes[i]
                ); <------
            }
          ...
        }

        winners[sessionId] = assertion.winners;
    }
```

As you can see the `recordResults` is calling the `recordResult` function for the specific strategies:
```solidity
 function recordResult(uint256 questionId, address player, uint256 xp, uint256 time) external {
        address sessionStrategy = SessionManager(revealedQuestions[questionId].sessionManager).getSessionStrategy(
            revealedQuestions[questionId].gameId
        );
        require(sessionStrategy == msg.sender, OnlySessionStrategy(sessionStrategy, msg.sender));

        results[questionId][player] = Result({xp: xp, time: time}); <------
    }
```

The problem is that the `recordResult` function is mean to savee the xp and time of the specific question of a gameId but what the `recordResults` function is passing the average of the user xp and time for all question corresponding to a specific gameId(sessionId).

**Impact:** Incorrect value passed for `recordResult` in all startgyes  this will return incorrect values in  `getResult` which is called in `_calculatePlayerSessionResult` and used as a view function.

**Majority Games:**
Fixed in commit [a3bcfb6](https://github.com/Engage-Protocol/engage-protocol/commit/a3bcfb6518f0eb33a6a37089e9e0a2c14ea7b210).

**Cyfrin:** Verified.
