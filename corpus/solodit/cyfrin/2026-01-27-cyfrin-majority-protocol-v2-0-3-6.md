---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-3-6
ingested_at: '2026-08-23T05:04:32Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Low
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: '`SessionManager::revealGameQuestion` doesn''t validate that input `_questionId`
  belongs to input `_gameId`'
vuln_class: []
---

# `SessionManager::revealGameQuestion` doesn't validate that input `_questionId` belongs to input `_gameId`

_Section severity (from Solodit section header): Low_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `SessionManager::revealGameQuestion` doesn't validate that input `_questionId` belongs to input `_gameId`. It calls `QuestionManager::_revealPrompt` which ends up calling the `revealQuestion` function of the relevant prompt contract, but none of these verify that the input `_questionId` belongs to input `_gameId`.

**Impact:** A game creator can bypass the requirement that a game must be in the `Ongoing` state in order to reveal questions, by calling `SessionManager::revealGameQuestion` with `_gameId` of another game that is in the `Ongoing` state even if their game is not.

**Recommended Mitigation:** * Verify that the input `_questionId` belongs to input `_gameId` and consider applying the same fix such that it is also enforced for `startAndRevealGameQuestion`. One way to do this is by adding this check inside `QuestionManager::_revealPrompt`:
```diff
    function _revealPrompt(uint256 _gameId, uint256 _questionId, bytes memory _prompt, uint256 _salt) internal {
        PromptInitData storage promptInitData = questionCommitment[_questionId];
+       require(
+               _gameId == promptInitData.sessionId,
+               InvalidSessionIdForQuestion(_questionId, _gameId, promptInitData.sessionId)
+       );
```

* Consider also restricting functions such as `startAndRevealGameQuestion` and `revealGameQuestion` using the `onlyCreator` modifier - though technically this shouldn't be strictly necessary as only the game creator possesses the necessary salts.

**Majority Games:**
Fixed in commit [15a2459](https://github.com/Engage-Protocol/engage-protocol/commit/15a24591dd9e1987e0f5383cc2d7de28e3072c77).

**Cyfrin:** Verified.

\clearpage
