---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-13
ingested_at: '2026-08-09T05:32:30Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`getReactionTime` is returning the `reactionDeadline` even if the user didn''t
  participate in the game'
vuln_class: []
---

# `getReactionTime` is returning the `reactionDeadline` even if the user didn't participate in the game

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** The `getReactionTime function` retrieves the reaction time for a player on a specific question:

```solidity
 function getReactionTime(uint256 questionId, address player) public view returns (uint256) {
        return _getReactionTime(questionId, player);
    }
    function _getReactionTime(uint256 questionId, address player) internal view returns (uint256) {
        return reactions[questionId][player].baseReaction.timestamp == 0
            ? revealedQuestions[questionId].reactionDeadline <------
            : reactions[questionId][player].baseReaction.timestamp - revealedAt[questionId];
    }
```

As you can see, if a user has never participated in the game, the function returns the maximum `reactionDeadline` for the question instead of reverting for a user who didn’t commit a response or participate in the game.

**Impact:** The `getReactionTime` function returns an incorrect value for a user who didn’t commit a response or participate in the game.

**Recommended Mitigation:** Consider return 0 or revert in `getReactionTime` if a user has never participated in a game.

**Majority Games:**
This is the intended behavior but we [updated](https://github.com/Engage-Protocol/engage-protocol/commit/9cacc0c94b6d9e343177d820accf6ceee5d387e8). the natspec to make this explicit now.

**Cyfrin:** Verified.

\clearpage
