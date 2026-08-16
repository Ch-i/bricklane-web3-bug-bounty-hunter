---
affected_contracts: []
derives_from: []
id: solodit-cyfrin-2026-01-27-cyfrin-majority-protocol-v2-0-4-6
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
title: Game creator can grief winners by cancelling the game once it has ended, preventing
  winners from receiving their rewards
vuln_class: []
---

# Game creator can grief winners by cancelling the game once it has ended, preventing winners from receiving their rewards

_Section severity (from Solodit section header): Informational_  
_Audit firm: Cyfrin_  
_Source report: [2026-01-27-cyfrin-majority-protocol-v2.0.md](https://github.com/solodit/solodit_content/blob/main/reports/Cyfrin/2026-01-27-cyfrin-majority-protocol-v2.0.md)_

---

**Description:** `SessionManager::cancelGame` allows the game creator to cancel the game when it is in the `Ended` state:
```solidity
function cancelGame(uint256 _gameId) external onlyCreator(_gameId) {
    require(
        games[_gameId].state != SessionState.Cancelled,
        InvalidGameState(SessionState.Cancelled, games[_gameId].state)
    );
    require(
        games[_gameId].state != SessionState.Concluded,
        InvalidGameState(SessionState.Concluded, games[_gameId].state)
    );
    games[_gameId].state = SessionState.Cancelled;
    emit GameCancelled(_gameId);
}
```

**Impact:** Once the game has ended but not yet concluded, the game creator can cancel if they don't like who the winners are. This griefs the winners preventing them from collecting their rewards.

**Recommended Mitigation:** Don't allow the game creator to cancel the game in the `Ended` state:
```diff
    function cancelGame(uint256 _gameId) external onlyCreator(_gameId) {
        require(
            games[_gameId].state != SessionState.Cancelled,
            InvalidGameState(SessionState.Cancelled, games[_gameId].state)
        );
+       require(
+           games[_gameId].state != SessionState.Ended,
+           InvalidGameState(SessionState.Ended, games[_gameId].state)
+       );
        require(
            games[_gameId].state != SessionState.Concluded,
            InvalidGameState(SessionState.Concluded, games[_gameId].state)
        );
        games[_gameId].state = SessionState.Cancelled;
        emit GameCancelled(_gameId);
    }
```

**Majority Games:**
Acknowledged due to the Oracle's inability to settle according to the calculation rules (e.g. crash happens).
