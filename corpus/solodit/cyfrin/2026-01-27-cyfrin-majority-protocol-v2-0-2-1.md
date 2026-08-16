---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-1
ingested_at: '2026-08-16T05:02:10Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`MajorityChoicePrompt`, `SPBinaryPrompt` and `TriviaChoicePrompt` will not
  work correctly when used with different instances of `SessionManager`'
vuln_class: []
---

# `MajorityChoicePrompt`, `SPBinaryPrompt` and `TriviaChoicePrompt` will not work correctly when used with different instances of `SessionManager`

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `MajorityChoicePrompt` is supposed to support multiple instances of `SessionManager`, however every instance of `SessionManager` starts with `QuestionManager::nextQuestionId = 0`.

This is problematic as `MajorityChoicePrompt::revealReaction` does this:
```solidity
Reaction storage r = reactions[_questionId][_user];
require(!r.baseReaction.reactions[_questionId][_user], AnswerAlreadyRevealed(_user, _gameId, _questionId));
```

When a user plays `questionId = 0` on the first instance of `SessionManager` everything will work ok and `reactions[_questionId][_user].revealed` will be set to `true`.

If that same user plays `questionId = 0` on a second instance of `SessionManager` which uses the same instance of `MajorityChoicePrompt`, then `MajorityChoicePrompt::revealReaction` will revert with `AnswerAlreadyRevealed`.

Another potential issue is that `results[questionId][player]` will have valid results stored for a player from games on the first instance and this mapping doesn't differentiate between the different instances of `SessionManager`.

**Recommended Mitigation:** The simplest fix is that each `SessionManager` instances gets its own fresh `MajorityChoicePrompt` instance; the same issue likely affects `SPBinaryPrompt` and `TriviaChoicePrompt`.

Another option is that:
* there should only be 1 active instance of `SessionManager` at one time
* when a new instance of `SessionManager` is made active, it should be initialized with `gameId`, `sessionId` and `questionId` that are greater than the previous active instance
* add tests to the test suite which exercise this exact scenario to ensure everything will continue to work as expected

**Majority Games:**
Fixed in commits [4b151db](https://github.com/Engage-Protocol/engage-protocol/commit/4b151db34ae5e0adb59076e472f292cfbeb9f571), [46d00d3](https://github.com/Engage-Protocol/engage-protocol/commit/46d00d3096a86694ccfa2b6ddec2ba90265e6ba2), [35c63e7](https://github.com/Engage-Protocol/engage-protocol/commit/35c63e77e829f48d6bb6b74bf6f3f5446399ec9b).

**Cyfrin:** Verified.
