---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-2-0
ingested_at: '2026-07-19T07:07:17Z'
protocol_category: []
published_at: '2026-01-27T00:00:00Z'
related_swc: []
severity: Medium
source: solodit
source_url: https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md
tags:
- firm:cyfrin
- report:2026-01-27-cyfrin-majority-protocol-v2-0
title: User can join after the first question is revealed to gain an advantage over
  other users
vuln_class: []
---

# User can join after the first question is revealed to gain an advantage over other users

_Section severity (from Solodit section header): Medium_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** Users can join a game while the game is ongoing:
```solidity
 function joinGame(uint256 _gameId) external {
        require(
            games[_gameId].state == SessionState.Created || games[_gameId].state == SessionState.Ongoing,
            InvalidGameState(SessionState.Created, games[_gameId].state)
        );
    }
```

`SessionManager::startAndRevealGameQuestion` both moves the game to the `Ongoing` state and reveals the first question.

**Impact:** A user can get an unfair advantage over others by always waiting for the first question to be revealed, and only joining a game if they know the answer to that question.

**Recommended Mitigation:** Consider don't allow user join to the game when the game is already ongoing:

```diff
  function joinGame(uint256 _gameId) external {
-      require(
-            games[_gameId].state == SessionState.Created || games[_gameId].state == SessionState.Ongoing,
-            InvalidGameState(SessionState.Created, games[_gameId].state)
-        );
+      require(
+            games[_gameId].state == SessionState.Created,
+            InvalidGameState(SessionState.Created, games[_gameId].state)
+        );
```

**Majority Games:**
Fixed in commit [6ec205f](https://github.com/Engage-Protocol/engage-protocol/commit/6ec205f68d5f0d2bcf25035d5da09fe859f065b7).

**Cyfrin:** Verified.
