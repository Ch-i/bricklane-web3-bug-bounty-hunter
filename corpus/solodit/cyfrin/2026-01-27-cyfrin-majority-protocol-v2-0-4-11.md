---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-11
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Informational
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`Prompt::gameId` is not validated to belong to the `questionId` and never
  used, could be removed'
vuln_class: []
---

# `Prompt::gameId` is not validated to belong to the `questionId` and never used, could be removed

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** When a creator creates a game they send an array of  bytes32 `promptHash` variables associate with the questions:
```solidity
 function createGame(
        uint256 _startTime,
        uint256 _endTime,
        uint256 _ticketPrice,
        uint256 _creatorFee,
        address _token,
        address _creatorFeeReceiver,
        bytes32[] memory _promptHashes, <-----
        address[] memory _promptStrategies,
        address _sessionStrategy,
        address _rewardStrategy,
        bool _verificationRequired
    ) external returns (uint256 gameId) {...}
```

These `promptHash` are then reveled in the `_revealPrompt` function when creator call `startAndRevealGameQuestion` or `revealGameQuestion`. `_revealPrompt` is checking `keccak256(abi.encodePacked(_prompt, _salt)) == promptInitData.promptHash` and calling `revealQuestion` in the strategies:

```solidity
 function revealQuestion(bytes memory question, uint256 questionId) external {
        Prompt memory q = abi.decode(question, (Prompt));  <------
        require(registry.engageProtocols(msg.sender), InvalidSessionManager(msg.sender));
        require(q.sessionManager == msg.sender, OnlySessionManager(q.sessionManager, msg.sender));
        (, address promptStrategy) = SessionManager(q.sessionManager).questionCommitment(questionId);
        require(promptStrategy == address(this), InvalidPromptCall(questionId, promptStrategy));
        revealedQuestions[questionId] = q;
        revealedAt[questionId] = block.timestamp;
    }
```

The bytes Prompt is decode and converted in the `Prompt`  struct:
```solidity
 struct Prompt {
        address sessionManager;
        uint256 gameId; <------
        string questionText;
        uint256 reactionDeadline;
        bytes32 solutionCommitment;
        uint16 solution;
        string[] media;
        string[] choices;
    }
```

Hence `gameId` is never validated to belong to that `questionId`. Is is also never read anywhere apart from one `view` function that is never used so it could be safely removed.

**Majority Games:**
Initially we removed it from the `Prompt` struct in commit [3644561](https://github.com/Engage-Protocol/engage-protocol/commit/36445618404482096f9170f605e88a7e7039a1bd). However it was later added back in commit [581a98d](https://github.com/Engage-Protocol/engage-protocol/commit/581a98d91b0246443f5c51bde665ae3641441fd3) as it was required to resolve issue `Prompt::finalizedAnswer is never set`.

**Cyfrin:** Verified.
