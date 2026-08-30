---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-3
ingested_at: '2026-08-30T10:05:51Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: Malicious user can front run the `revealSolutions` call committing the correct
  solution
vuln_class: []
---

# Malicious user can front run the `revealSolutions` call committing the correct solution

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** A malicious user can front run the `revealSolutions` solution call taking the solution and committing the correct solution before the `revealSolutions`  txn get through.

```solidity
 function commitReaction(uint256 _gameId, uint256 _questionId, bytes32 _commit, address _user) external {

        require(solutionRevealedAt[_questionId] == 0, SolutionAlreadyRevealed(_questionId));  <----
        require(
            revealedAt[_questionId] + revealedQuestions[_questionId].reactionDeadline > block.timestamp,
            ReactionDeadlinePassed(_user, _questionId)
        ); <----
       ...

        r.baseReaction.commit = _commit;
        r.baseReaction.timestamp = block.timestamp;

        emit AnswerCommitted(_gameId, _questionId, _user, _commit);
    }
```

A malicious user can just wait until the solution is reveled and  commit the correct solution as long as this condition is met:
`revealedAt[_questionId] + revealedQuestions[_questionId].reactionDeadline > block.timestamp`.

There is not check in  `revealSolutions` that can prevent the reveal the solution too early.

**Impact:** Malicious can wait until the  `revealSolutions` is called to commit the correct solution. Base has no mempool however.

**Majority Games:**
Acknowledged.
